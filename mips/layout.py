from visual.layouts import *

class MIPSColumnLayout(ColumnLayoutManager):
  def __init__(self, arch):
    super(MIPSColumnLayout, self).__init__(arch, arch.pc)
    arch.pc.name = "PC"
    arch.control.name = "Control Unit"
    arch.alu.name = "ALU"
