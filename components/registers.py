from component import *
from ..simulator import Delta
from bitstring import BitArray
import math

class DRegister(ParametrizedComponent):
  delay = 100
  parameters  = {'width': 8}
  inputs = {'q': 'width'}
  outputs = {'d': 'width'}

  def simulate(self, ports):
    if 'q' in ports:
      self.d.data = BitArray(self.q.data)
      return self.changed(self.d)

DRegister32 = DRegister.with_parameters(width = 32)
