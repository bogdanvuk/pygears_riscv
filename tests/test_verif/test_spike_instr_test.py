from pygears_riscv.riscv.riscv import ADDI
from pygears_riscv.verif.spike_instr_test import disassemble, run_all


def test_dissasembly():
    assert disassemble(ADDI) == "addi x0, x0, 0"

    instr1 = ADDI.replace(imm=1234, rd=22, rs1=0)
    assert disassemble(instr1) == "addi x22, x0, 1234"


def test_addi():
    test_instr = ADDI.replace(imm=1234, rd=22, rs1=0)
    reg_values = run_all([test_instr], outdir='build')
    assert(reg_values[22] == 1234)
