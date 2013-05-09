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

# Note: Write before Read
class RegisterFile(ParametrizedComponent):
  delay = 500

  parameters = {'num_regs': 16, 'width': 32}

  inputs  = {'read_reg1' : 'log_num_regs', 'read_reg2' : 'log_num_regs',
             'write_reg' : 'log_num_regs', 'write': 'width',
             'reg_write': 1}

  outputs = {'read1': 'width', 'read2': 'width'}

  @classmethod
  def process_parameters(klass, params):
    params['log_num_regs'] = int(math.ceil(math.log(params['num_regs'], 2)))

  def __init__(self, **kwargs):
    Component.__init__(self, **kwargs)
    self.registers = []
    while xrange(self.parameters['num_regs']):
      self.registers.append(BitArray(length = params['width']))

  def simulate(self, ports):
    changes = []
    if self.reg_write.int == 1:
      self.registers[self.write_reg.data.uint] = BitArray(self.write.data)
    if 'read_reg1' in ports:
      self.read1.data = BitArray(self.registers[self.read_reg1.data.uint])
      changes.append(self.read1)
    if 'read_reg2' in ports:
      self.read2.data = BitArray(self.registers[self.read_reg2.data.uint])
      changes.append(self.read2)

    return self.changed(*changes)
