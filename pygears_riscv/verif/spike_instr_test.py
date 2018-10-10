import os
from spike import Spike
from riscv import OP_IMM, FUNCT3_ADDI

instruction_names = {OP_IMM: {FUNCT3_ADDI: 'addi'}}


def disassemble(instruction):
    if instruction['opcode'] == OP_IMM:
        name = instruction_names[OP_IMM][instruction['funct3']]

        return (f'{name} x{int(instruction["rd"])},'
                f' x{int(instruction["rs1"])}, '
                f' {int(instruction["imm"])}')

    else:
        raise Exception("Unsupported")


linker_script = '''SECTIONS
{
. = 0x80000000;
}'''

assembly_template = """
;; # Assembly program template.

.text
  .global _start

_start:

  ;; # The actual instructions I'd like to test.
  {0}

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
fromhost: .dword 0
"""


class SpikeInstrTest(Spike):
    def __init__(self, instructions, outdir='.'):
        outdir = os.path.abspath(
            os.path.expandvars(os.path.expanduser(outdir)))
        asm_file_name = os.path.join(outdir, 'instr_test.s')
        self.out_file_name = os.path.join(outdir, 'instr_test')
        ld_file_name = os.path.join(outdir, 'instr_test.ld')

        with open(ld_file_name, 'w') as f:
            f.write(linker_script)

        self.instructions = instructions
        asm_instructions = map(disassemble, instructions)

        with open(asm_file_name, 'w') as f:
            f.write(assembly_template.format('\n'.join(asm_instructions)))

        gcc_cmd = (f'riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32'
                   f' -nostdlib -T {ld_file_name} {asm_file_name}'
                   f' -o {self.out_file_name}')

        os.system(gcc_cmd)

        super().__init__(f'spike -d --isa=rv32i {self.out_file_name}')

    def run_all(self):
        self.until(len(self.instructions) * 4)
        return [self.reg(i) for i in range(32)]


def run_all(instructions, outdir='.'):
    with SpikeInstrTest(instructions, outdir) as sp:
        return sp.run_all()
