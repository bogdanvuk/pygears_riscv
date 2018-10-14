import jinja2
import os
from pygears_riscv.verif.spike import Spike
from pygears_riscv.riscv.riscv import OPCODE_IMM, FUNCT3_ADDI

instruction_names = {OPCODE_IMM: {FUNCT3_ADDI: 'addi'}}


def disassemble(instruction):
    if instruction['opcode'] == OPCODE_IMM:
        name = instruction_names[OPCODE_IMM][instruction['funct3']]

        return (f'{name} x{int(instruction["rd"])},'
                f' x{int(instruction["rs1"])},'
                f' {int(instruction["imm"])}')

    else:
        raise Exception("Unsupported")


linker_script = '''SECTIONS
{
. = 0x80000000;
}'''

assembly_template_string = """
;; # Assembly program template.

.text
  .global _start

_start:
{% for reg, value in reg_set_init.items() %}
.equ X{{ reg }}_INIT_VALUE, {{ value }}
{%- endfor %}

  ;; # Optional preloading of initial register values.
{% for reg in reg_set_init %}
  lui x{{ reg }},      %hi(X{{ reg }}_INIT_VALUE)
  addi x{{ reg }}, x{{ reg }}, %lo(X{{ reg }}_INIT_VALUE)
{%- endfor %}

  ;; # The actual instructions I'd like to test.
{% for instruction in instructions %}
  {{ disassemble(instruction) }}
{%- endfor %}

  ;; # Write the value 1 to tohost, telling Spike to quit with 0 exit code.
  li t0, 1
  la t1, tohost
  sw t0, 0(t1)

  ;; # Spin until Spike terminates the simulation.
  1: j 1b

;; # Expose tohost and fromhost to Spike so we can communicate with it.
.data
  .global tohost
tohost:   .dword 0
  .global fromhost
fromhost: .dword 0"""


class SpikeInstrTest(Spike):
    def __init__(self, instructions, outdir='.', reg_set_init={}):
        outdir = os.path.abspath(
            os.path.expandvars(os.path.expanduser(outdir)))
        asm_file_name = os.path.join(outdir, 'instr_test.s')
        self.out_file_name = os.path.join(outdir, 'instr_test')
        ld_file_name = os.path.join(outdir, 'instr_test.ld')
        log_file_name = os.path.join(outdir, 'instr_test.log')

        os.makedirs(outdir, exist_ok=True)

        with open(ld_file_name, 'w') as f:
            f.write(linker_script)

        self.instructions = instructions
        self.reg_set_init = reg_set_init

        with open(asm_file_name, 'w') as f:
            assembly_template = jinja2.Environment().from_string(
                assembly_template_string)

            f.write(
                assembly_template.render(
                    reg_set_init=reg_set_init,
                    disassemble=disassemble,
                    instructions=instructions))

        gcc_cmd = (f'riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32'
                   f' -nostdlib -T {ld_file_name} {asm_file_name}'
                   f' -o {self.out_file_name}'
                   f' > {log_file_name} 2>&1')

        os.system(gcc_cmd)

        super().__init__(f'spike -d --isa=rv32i {self.out_file_name}')

    def reg_set_read(self):
        return [self.reg(i) & 0xffffffff for i in range(32)]

    @property
    def reg_set_initialization_instr_num(self):
        '''Returns the number of instructions needed for the register set
        initialization'''

        return len(self.reg_set_init) * 2

    def run_all(self):
        self.step(self.reg_set_initialization_instr_num)
        reg_set_start = self.reg_set_read()
        self.step(len(self.instructions))
        reg_set_end = self.reg_set_read()

        return reg_set_start, reg_set_end


def run_all(instructions, outdir='.', reg_set_init={}):
    with SpikeInstrTest(instructions, outdir, reg_set_init=reg_set_init) as sp:
        return sp.run_all()
