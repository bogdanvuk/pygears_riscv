import os
from pygears_riscv.verif.env import riscv_instr_seq_env
from pygears.sim.extens import graphviz

img_file_name = os.path.expanduser(
    '~/pygears/docs/blog/riscv/images/riscv_graph_addi.png')

riscv_instr_seq_env(instr_seq=[], xlen=32)

graph = graphviz.graph(edge_fmt='{prod_gear} -> {cons_gear}')

for edge in graph.cons_edge_map.values():
    edge.set_penwidth(2)

graph.write_png(img_file_name)
