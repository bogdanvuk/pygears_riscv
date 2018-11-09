from pygears.sim import sim
from pygears.typing import Int

from pygears_riscv.riscv.riscv import SLTI

from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears_riscv.verif import spike_instr_test


from pygears.typing_common import cast


def test_slti():
    test_instr = SLTI.replace(imm=-2, rd=1, rs1=1)

    reg_file_init = {1: -1}

    spike_reg_file_start, spike_reg_file_end = spike_instr_test.run_all(
        [test_instr], outdir='build', reg_file_init=reg_file_init)

    reg_file_mem = riscv_instr_seq_env(
        instr_seq=[test_instr],
        xlen=32,
        reg_file_mem=dict(enumerate(spike_reg_file_start)))

    sim()

    print(
        f'Resulting value of the register x1: {cast(reg_file_mem[1], Int[32])}'
    )

    for reg_id, reg_value in reg_file_mem.items():
        assert spike_reg_file_end[reg_id] == reg_value
