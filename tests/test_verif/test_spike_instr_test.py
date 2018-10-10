from spike_instr_test import run_all


test_instr = ADDI.replace(imm=1234, rd=22, rs1=0)
run_all()
