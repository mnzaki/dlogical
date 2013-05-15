from component import *
import math

class Mem(ParametrizedComponent):
  delay = 400
  shape = Rectangle(200, 300)

  parameters = {'width': 32, 'size': 1024 }

  inputs  = {'addr':     'log_size',
             'write':    'width',
             'write_en': 1,
             'read_en':  1}

  outputs = {'read':     'width'}

  @classmethod
  def process_parameters(klass, params):
    params['log_size'] = int(math.ceil(math.log(params['size'], 2)))

  def __init__(self, mem = None, **kwargs):
    mem = mem or [0] * self.parameters['size']
    self.mem = mem
    Component.__init__(self, **kwargs)

  def simulate(self, ins, outs):
    addr = (self.addr.data * 8) / self.parameters['width']
    if self.write_en.data == 1 and addr < len(self.mem):
      self.mem[addr] = self.write.data
    if self.read_en.data == 1:
      if addr > len(self.mem):
        outs.read = 0
      else:
        outs.read = self.mem[addr]
