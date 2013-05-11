from component import *
import math

class Mem(ParametrizedComponent):
  delay = 400

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
    if self.write_en.data == 1:
      self.mem[self.addr.data] = self.write.data
    if self.read_en.data == 1:
      outs.read = self.mem[self.addr.data]
