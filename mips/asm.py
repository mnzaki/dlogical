# insprired by http://pythonwise.blogspot.com/2012/06/python-based-assembler.html
# and has since diverged dramatically

CLEAN_ENV = {} #globals().copy()

from array import array
from bitstring import BitArray

# 32bit Instruction Format
OPCODE_SLICE = slice(0, 6)
DATA_SLICE   = slice(6, 32)
RS_SLICE     = slice(6, 11)
RT_SLICE     = slice(11, 16)
RD_SLICE     = slice(16, 21)
SHAMT_SLICE  = slice(21, 26)
FUNCT_SLICE  = slice(26, 32)
IMM_SLICE    = slice(16, 32)

class ASM(object):
  instruction_set = {}
  program = None

class Instruction(object):
  @classmethod
  def new(klass, name, opcode = None):
    if opcode is None:
      opcode = klass.opcode
    instr = type(name, (klass,), dict(opcode = opcode))
    ASM.instruction_set[name] = instr
    return instr

  def __init__(self):
    ASM.program.append(self)

  def bin(self):
    b = BitArray(32)
    b[OPCODE_SLICE] = self.opcode
    self._gen_data(b)
    return b.uint

class RFormat(Instruction):
  opcode = 0b000000

  instructions = {
    'add':  0b100000,
    'sub':  0b100010,
    'and_': 0b100100,
    'or_':  0b100101,
    'slt':  0b101010,
    'nor':  0b100111
  }

  @classmethod
  def new(klass, name, funct):
    instr = super(RFormat, klass).new(name, klass.opcode)
    instr.funct = funct
    return instr

  def __init__(self, rd, rs, rt):
    super(RFormat, self).__init__()
    self.rd = rd
    self.rs = rs
    self.rt = rt
    self.shamt = 0
  def _gen_data(self, b):
    b[RS_SLICE] = self.rs
    b[RT_SLICE] = self.rt
    b[RD_SLICE] = self.rd
    b[SHAMT_SLICE] = self.shamt
    b[FUNCT_SLICE] = self.funct

class jr(RFormat):
  funct = 0b001000
  def __init__(self, rs):
    RFormat.__init__(self, 0, rs, 0)

class Shifts(RFormat):
  instructions = {
    'sll': 0b000000,
    'srl': 0b000010
  }

  def __init__(self, rd, rt, shamt):
    super(Shifts, self).__init__(rd, 0, rt)
    self.shamt = shamt

class IFormat(Instruction):
  instructions = {
    'lw':   0b100011,
    'sw':   0b101011,
    'addi': 0b001000,
    'ori':  0b001101,
    'andi': 0b001100
  }

  def __init__(self, rt, rs, imm):
    super(IFormat, self).__init__()
    self.rs = BitArray(length = 5, uint = rs)
    self.rt = BitArray(length = 5, uint = rt)
    self.imm = imm
  def _gen_data(self, b):
    b[RS_SLICE] = self.rs
    b[RT_SLICE] = self.rt

    if isinstance(self.imm, Label):
      self.imm = self.imm.relative(self)
    if self.imm > 0:
      self.imm = BitArray(length = 16, uint = self.imm)
    else:
      self.imm = BitArray(length = 16, int = self.imm)

    b[IMM_SLICE] = self.imm

class FlippedIFormat(IFormat):
  instructions = {
    'beq':  0b000100,
    'bne':  0b000101,
  }
  def __init__(self, rs, rt, imm):
    super(FlippedIFormat, self).__init__(rt, rs, imm)
  def _gen_data(self, b):
    super(FlippedIFormat, self)._gen_data(b)

class JFormat(Instruction):
  instructions = {
    'j':   0b000010,
    'jal': 0b000011
  }

  def __init__(self, address):
    super(JFormat, self).__init__()
    self.address = address
  def _gen_data(self, b):
    if isinstance(self.address, Label):
      self.address = self.address.absolute()
    b[DATA_SLICE] = self.address

for fmt in [RFormat, Shifts, IFormat, FlippedIFormat, JFormat]:
  for k, v in fmt.instructions.iteritems():
    fmt.new(k, v)
ASM.instruction_set['jr'] = jr

class Label(object):
  def __init__(self, pos = None):
    self.update(pos)
  def update(self, pos = None):
    if pos is None:
      pos = len(ASM.program)
    self.pos = pos
  def relative(self, inst):
    return self.pos - ASM.program.index(inst) - 1
  def absolute(self):
    return self.pos

class AssemblerEnvironment(dict):
  def label(self, name):
    if name in self:
      self[name].update()
    else:
      self[name] = Label()

  def define_labels(self, *args):
    for l in args:
      self[l] = Label()

  def __init__(self):
    dict.__init__(self, CLEAN_ENV)

    # registers $t0 - $t7 are 8 - 15
    for i in xrange(8, 16):
        self['t%d' % (i - 8)] = i
    # registers $t8 - $t9 are 24 - 25
    for i in xrange(24, 26):
        self['t%d' % (i - 16)] = i
    # registers $s0 - $s7 are 16 - 23
    for i in xrange(16, 24):
        self['s%d' % (i - 16)] = i
    # $zero
    self['zero'] = 0
    # $ra
    self['ra'] = 31

    # Instructions
    for name, inst in ASM.instruction_set.iteritems():
        self[name] = inst

    # program keeping and special cases
    self['program'] = []
    self['label'] = self.label
    self['define_labels'] = self.define_labels

class Assembler(object):
  def assemble(self, fname):
    env = AssemblerEnvironment()
    ASM.program = env['program']
    execfile(fname, env, {})

    program = map(Instruction.bin, env['program'])
    return array('L', program)
