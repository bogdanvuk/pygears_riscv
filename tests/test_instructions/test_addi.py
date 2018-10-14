from pygears.sim import sim

from pygears_riscv.riscv.riscv import ADDI, TInstructionI

from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears_riscv.verif import spike_instr_test


def test_addi():
    # reg_set_init = {1: 1234}
    reg_set_init = {1: -1}
    test_instr = ADDI.replace(imm=-1235, rd=1, rs1=1)

    spike_reg_set_start, spike_reg_set_end = spike_instr_test.run_all(
        [test_instr], outdir='build', reg_set_init=reg_set_init)

    reg_file_mem = riscv_instr_seq_env(
        instr_t=TInstructionI,
        instr_seq=[test_instr],
        xlen=32,
        reg_file_mem=dict(enumerate(spike_reg_set_start)))

    sim()

    for reg_id, reg_value in reg_file_mem.items():
        assert spike_reg_set_end[reg_id] == reg_value

test_addi()
