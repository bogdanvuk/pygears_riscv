import os
from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears_riscv.riscv.riscv import ADDI, TInstructionI
from pygears.sim import sim
from pygears.sim.extens import sim_timelapse
from functools import partial

gif_delay = 120
addi_timelapse_dir = os.path.expanduser('~/pygears/docs/blog/riscv/images')
timelapse_gif_name = 'addi-timelapse'

riscv_instr_seq_env(
    instr_seq=[ADDI.replace(imm=-1233, rd=1, rs1=1)],
    xlen=32,
    reg_file_mem={1: -1})

sim(extens=[
    partial(
        sim_timelapse.SimTimelapse,
        outdir=os.path.join(addi_timelapse_dir, timelapse_gif_name))
])

os.chdir(addi_timelapse_dir)

os.system(f"convert -delay {gif_delay} -loop 0 "
          f"{timelapse_gif_name}/*.gif {timelapse_gif_name}.gif")

os.system(f"convert {timelapse_gif_name}.gif -coalesce"
          f" -pointsize 40"
          f" -gravity NorthWest -annotate +20+20"
          f" \"Timestep: %[fx:floor(t/18)] Delta: %[fx:t%18]\""
          f" -layers Optimize {timelapse_gif_name}.gif")
