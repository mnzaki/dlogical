from ..components.component import *

class ALU(Component):
  delay = 500

  inputs = {'in0': 32, 'in1': 32, 'control': 4}
  outputs = {'out': 1}

  # FIXME check changes?
  def simulate(self, ins, outs):
    if self.control.data == 0:
      outs.out = self.in0.data & self.in1.data
    elif self.control.data == 1:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == 2:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == 3:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == 4:
      outs.out = self.in0.data + self.in1.data
    elif self.control.data == 5:
      outs.out = self.in0.data + self.in1.data
