from pygears.sim import sim

from riscv import ADDI, TInstructionI

from riscv_verif import riscv_instr_seq_env


def test_addi():

    test_instr = ADDI.replace(imm=1234, rd=22, rs1=0)

    reg_file_mem = riscv_instr_seq_env(
        instr_t=TInstructionI, instr_seq=[test_instr], xlen=32)

    # sim(extens=[sim_timelapse.SimTimelapse])
    sim()
