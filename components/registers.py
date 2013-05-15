from component import *
from simulator import Delta
import math

class DRegister(ParametrizedComponent):
  delay = 100
  shape = Rectangle(150, 200)

  parameters = {'width': 8}
  inputs = {'q': 'width'}
  outputs = {'d': 'width'}

  def simulate(self, inputs, outputs):
    if 'q' in inputs:
      outputs.d = inputs.q

DRegister32 = DRegister.with_parameters(width = 32)

# Positive edge triggered D register
class DRegisterSync(DRegister):
  inputs = {'q': 'width',
            'clk': 1}

  def simulate(self, ins, outs):
    if 'clk' in ins and ins.clk == 1:
      outs.d = self.q.data

DRegisterSync32 = DRegisterSync.with_parameters(width = 32)

# Note: Write before Read
class RegisterFile(ParametrizedComponent):
  delay = 500
  shape = Rectangle(200, 300)

  parameters = {'num_regs': 16, 'width': 32}

  inputs  = {'read_reg1' : 'log_num_regs', 'read_reg2' : 'log_num_regs',
             'write_reg' : 'log_num_regs', 'write': 'width',
             'write_en': 1}

  outputs = {'read1': 'width', 'read2': 'width'}

  @classmethod
  def process_parameters(klass, params):
    params['log_num_regs'] = int(math.ceil(math.log(params['num_regs'], 2)))

  def __init__(self, **kwargs):
    Component.__init__(self, **kwargs)
    self.registers = [0] * self.parameters['num_regs']

  def simulate(self, inputs, outputs):
    if ('write' in inputs or 'write_reg' in inputs) and self.write_en.data == 1:
      self.registers[self.write_reg.data] = self.write.data
      if self.read_reg1.data == self.write_reg.data:
        outputs.read1 = self.write.data
      elif self.read_reg2.data == self.write_reg.data:
        outputs.read2 = self.write.data
    if 'read_reg1' in inputs:
      outputs.read1 = self.registers[inputs.read_reg1]
    if 'read_reg2' in inputs:
      outputs.read2 = self.registers[inputs.read_reg2]

# Synchronous write positive edge triggered register file
class RegisterFileSync(RegisterFile):
  inputs = RegisterFile.inputs.copy()
  inputs['clk'] = 1

  def simulate(self, inputs, outputs):
    if 'clk' in inputs and inputs.clk == 1:
      self.registers[self.write_reg.data] = self.write.data
    outputs.read1 = self.registers[self.read_reg1.data]
    outputs.read2 = self.registers[self.read_reg2.data]
