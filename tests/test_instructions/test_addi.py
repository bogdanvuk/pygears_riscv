from pygears.sim import sim

from pygears_riscv.riscv.riscv import ADDI, TInstructionI

from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears_riscv.verif import spike_instr_test


def test_addi():

    test_instr = ADDI.replace(imm=1234, rd=1, rs1=0)

    reg_file_mem = riscv_instr_seq_env(
        instr_t=TInstructionI, instr_seq=[test_instr], xlen=32)

    sim()

    spike_reg_values = spike_instr_test.run_all([test_instr], outdir='build')

    for reg_id, reg_value in reg_file_mem.items():
        assert spike_reg_values[reg_id] == reg_value
