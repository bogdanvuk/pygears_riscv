from pygears import Intf
from pygears.sim.modules import drv
from pygears.typing import Uint

from pygears_riscv.riscv.riscv import riscv, TInstructionI
from pygears_riscv.verif.register_file import register_file


def riscv_instr_seq_env(instr_seq, xlen=32, reg_file_mem={}):
    """Drives riscv with an instruction sequence.

    Args:
       instr_seq: Sequence of instructions to send to riscv, encoded as
           :py:data:`TInstructionI`

    Keyword Args:
       xlen (int): Width of the riscv registers in bits
       reg_file_mem (dict): Initial register file dictionary that maps
           register IDs to their initial values

    Returns:
       reg_file_mem
    """

    instruction = drv(t=TInstructionI, seq=instr_seq)

    reg_rd_data = Intf(Uint[xlen])

    reg_file_rd_req, reg_file_wr_req = riscv(instruction, reg_rd_data)

    reg_rd_data |= \
        register_file(reg_file_rd_req, reg_file_wr_req, storage=reg_file_mem)

    return reg_file_mem
