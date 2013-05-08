from component import *
from ..simulator import Delta

class DRegister(ParametrizedComponent):
  delay = 100
  parameters  = {'width': 8}
  inputs = {'q': 'width'}
  outputs = {'d': 'width'}

  def simulate(self):
    self.d.data = self.q.data.copy()
    return Delta(self.delay, [self.d])

DRegister32 = DRegister.with_parameters(width = 32)
