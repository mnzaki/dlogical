from ..components.component import *

class ALU(Component):
  delay = 500

  inputs = {'in0': 32, 'in1': 32, 'control': 4}
  outputs = {'out': 1}

  # FIXME check changes?
  def simulate(self, ins, outs):
    if self.control.data == 0b0000:
      outs.out = self.in0.data & self.in1.data
    elif self.control.data == 0b0001:
      outs.out = self.in0.data | self.in1.data
    elif self.control.data == 0b0010:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == 0b0110:
      outs.out = self.in0.data - self.in1.data
    elif self.control.data == 0b0111:
      outs.out = self.in0.data < self.in1.data #FIXME?
    elif self.control.data == 0b1100:
      outs.out = ~(self.in0.data | self.in1.data)
