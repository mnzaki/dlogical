from visual.layouts import *

class MIPSColumnLayout(ColumnLayoutManager):
  def __init__(self, arch):
    arch.pc.name = "PC"
    arch.pc.layout = self.layout(1)
    arch.pc.layout.relayout = 1
    arch.control.name = "Control Unit"
    arch.alu.name = "ALU"
    super(MIPSColumnLayout, self).__init__(arch)
