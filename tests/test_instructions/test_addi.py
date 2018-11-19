from pygears.sim import sim
from pygears.typing import Int, cast

from pygears_riscv.riscv.riscv import ADDI

from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears_riscv.verif import spike_instr_test

from pygears.sim.modules.verilator import SimVerilated
from pygears import find


def test_addi():
    test_instr = ADDI.replace(imm=-1233, rd=1, rs1=1)

    reg_file_init = {1: -1}

    spike_reg_file_start, spike_reg_file_end = spike_instr_test.run_all(
        [test_instr], outdir='build', reg_file_init=reg_file_init)

    reg_file_mem = riscv_instr_seq_env(
        instr_seq=[test_instr],
        xlen=32,
        reg_file_mem=dict(enumerate(spike_reg_file_start)))

    from pygears.sim.extens.vcd import VCD
    sim(extens=[VCD], outdir='/tools/home/tmp')

    print(
        f'Resulting value of the register x1: {cast(reg_file_mem[1], Int[32])}'
    )

    for reg_id, reg_value in reg_file_mem.items():
        assert spike_reg_file_end[reg_id] == reg_value


def test_addi_verilator():
    test_instr = ADDI.replace(imm=-1233, rd=1, rs1=1)

    reg_file_init = {1: -1}

    spike_reg_file_start, spike_reg_file_end = spike_instr_test.run_all(
        [test_instr], outdir='build', reg_file_init=reg_file_init)

    reg_file_mem = riscv_instr_seq_env(
        instr_seq=[test_instr],
        xlen=32,
        reg_file_mem=dict(enumerate(spike_reg_file_start)))

    find('/riscv').params['sim_cls'] = SimVerilated
    sim("build")

    print(
        f'Resulting value of the register x1: {cast(reg_file_mem[1], Int[32])}'
    )

    for reg_id, reg_value in reg_file_mem.items():
        assert spike_reg_file_end[reg_id] == reg_value
