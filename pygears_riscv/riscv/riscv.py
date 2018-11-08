from pygears import gear
from pygears.typing import Tuple, Uint, Int
from pygears.common import ccat

TInstructionI = Tuple[{
    'opcode': Uint[7],
    'rd': Uint[5],
    'funct3': Uint[3],
    'rs1': Uint[5],
    'imm': Int[12]
}]

OPCODE_IMM = 0x13
FUNCT3_ADDI = 0x000
FUNCT3_SLTI = 0b010

ADDI = TInstructionI({
    'opcode': OPCODE_IMM,
    'rd': 0,
    'funct3': FUNCT3_ADDI,
    'rs1': 0,
    'imm': 0
})

SLTI = TInstructionI({
    'opcode': OPCODE_IMM,
    'rd': 0,
    'funct3': FUNCT3_SLTI,
    'rs1': 0,
    'imm': 0
})


@gear
def riscv(instruction: TInstructionI, reg_data: Uint['xlen']):

    reg_file_rd_req = instruction['rs1']

    reg_data_signed = reg_data | Int[int(reg_data.dtype)]

    add_res = (reg_data_signed + instruction['imm']) \
        | reg_data.dtype

    reg_file_wr_req = ccat(instruction['rd'], add_res)

    return reg_file_rd_req, reg_file_wr_req
