import pexpect

abi_reg_names = {
    0: 'zero',
    1: 'ra',
    2: 'sp',
    3: 'gp',
    4: 'tp',
    5: 't0',
    6: 't1',
    7: 't2',
    8: 's0',
    9: 's1',
    10: 'a0',
    11: 'a1',
    12: 'a2',
    13: 'a3',
    14: 'a4',
    15: 'a5',
    16: 'a6',
    17: 'a7',
    18: 's2',
    19: 's3',
    20: 's4',
    21: 's5',
    22: 's6',
    23: 's7',
    24: 's8',
    25: 's9',
    26: 's10',
    27: 's11',
    28: 't3',
    29: 't4',
    30: 't5',
    31: 't6',
}


class Spike:
    PROMPT = r': $'
    CODE_BASE_ADDRESS = 0xffffffff80000000

    def __init__(self, cmd_line):
        self.cmd_line = cmd_line

    def __enter__(self):
        self.proc = pexpect.spawnu(self.cmd_line)
        self.proc.expect(Spike.PROMPT)
        self.proc.setecho(False)
        self.until(0)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.proc.close()

    def command(self, cmd):
        self.proc.sendline(cmd)
        self.proc.expect(Spike.PROMPT)
        return self.proc.before.strip()

    def until(self, address: int):
        self.command(f'until pc 0 {hex(Spike.CODE_BASE_ADDRESS + address)}')

    def pc(self) -> int:
        return int(self.command(f'pc 0'), 16) - Spike.CODE_BASE_ADDRESS

    def step(self):
        self.command('run 1')

    def reg(self, reg_id) -> int:
        return int(self.command(f'reg 0 {abi_reg_names[reg_id]}'), 16)
