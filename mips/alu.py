from ..components.component import *

class ALU(Component):
  AND_OP = 0b0000
  OR_OP  = 0b0001
  ADD_OP = 0b0010
  SUB_OP = 0b0110
  SLT_OP = 0b0111
  NOR_OP = 0b1100

  delay = 500

  inputs = {'in0': 32, 'in1': 32, 'control': 4}
  outputs = {'out': 1}

  # FIXME check changes?
  def simulate(self, ins, outs):
    if self.control.data == self.AND_OP:
      outs.out = self.in0.data & self.in1.data
    elif self.control.data == self.OR_OP:
      outs.out = self.in0.data | self.in1.data
    elif self.control.data == self.ADD_OP:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == self.SUB_OP:
      outs.out = self.in0.data - self.in1.data
    elif self.control.data == self.SLT_OP:
      outs.out = self.in0.data < self.in1.data #FIXME?
    elif self.control.data == self.NOR_OP:
      outs.out = ~(self.in0.data | self.in1.data)
