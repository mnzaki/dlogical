from component import Component
from ..simulator import Delta

class DRegister32(Component):
  delay = 100
  inputs = {'q': 32}
  outputs = {'d': 32}

  def __init__(self, **kwargs):
    super(DRegister32, self).__init__(**kwargs)

  def simulate(self):
    self.d.data = self.q.data.copy()
    return Delta(self.delay, [self.d])
