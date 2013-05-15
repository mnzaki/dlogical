from components.component import *
from alu import ALU

# This is the main control unit implemented as per the diagram
# on page 24 of Lecture 5 and the opcode map at the end of:
# https://www.student.cs.uwaterloo.ca/~isg/res/mips/opcodes

class ControlUnit(Component):
  delay = 200

  inputs  = {'opcode':   6,
             'funct':    6
            }
  outputs = {'regdst':   1,
             'jump':     1,
             'branch':   1,
             'memread':  1,
             'memtoreg': 1,
             'aluop':    2,
             'memwrite': 1,
             'alusrc':   1,
             'regwrite': 1,
             'beq_ne':   1,
             'regtopc':  1,
             'pctora':   1
            }

  def simulate(self, ins, outs):
    is_rfmt = self.opcode.data == 0b000000
    is_ifmt = self.opcode.data >  0b000111
    is_lw   = self.opcode.data == 0b100011
    is_sw   = self.opcode.data == 0b101011
    is_beq  = self.opcode.data == 0b000100
    is_bne  = self.opcode.data == 0b000101
    is_brn  = is_beq | is_bne
    is_j    = self.opcode.data == 0b000010
    is_jal  = self.opcode.data == 0b000011
    is_jr   = self.funct.data  == 0b001000

    outs.regdst = is_rfmt
    outs.jump = is_j | is_jal
    outs.branch = is_brn
    outs.memread = is_lw
    outs.memtoreg = is_lw
    outs.memwrite = is_sw
    outs.alusrc = is_ifmt
    outs.regwrite = (is_rfmt & (not is_jr)) | (is_ifmt & (not is_brn)) | is_jal | is_jr
    outs.beq_ne = is_beq
    outs.regtopc = is_jr
    outs.pctora  = is_jal

    if is_lw or is_sw:
      outs.aluop = 0b00
    elif is_brn or is_j | is_jal:
      outs.aluop = 0b01
    elif is_rfmt:
      outs.aluop = 0b10
    elif is_ifmt:
      outs.aluop = 0b11

# This has been extended to accept an op of 0b11 which signals setting of
# alucontrol based on opcode for supporting I-Format instructions

class ALUControlUnit(Component):
  delay = 200

  inputs  = {'aluop':      2,
             'funct':      6,
             'opcode':     6}

  outputs = {'alucontrol': 4}

  def simulate(self, ins, outs):
    if self.aluop.data == 0b00:
      outs.alucontrol = ALU.ADD_OP
    elif self.aluop.data == 0b01:
      outs.alucontrol = ALU.SUB_OP
    elif self.aluop.data == 0b10:
      if self.funct.data == 0b000000:
        outs.alucontrol = ALU.SLL_OP
      elif self.funct.data == 0b000010:
        outs.alucontrol = ALU.SRL_OP
      elif self.funct.data == 0b100000 or self.funct.data == 0b001000:
        outs.alucontrol = ALU.ADD_OP
      elif self.funct.data == 0b100010:
        outs.alucontrol = ALU.SUB_OP
      elif self.funct.data == 0b100100:
        outs.alucontrol = ALU.AND_OP
      elif self.funct.data == 0b100101:
        outs.alucontrol = ALU.OR_OP
      elif self.funct.data == 0b101010:
        outs.alucontrol = ALU.SLT_OP
      elif self.funct.data == 0b100111:
        outs.alucontrol = ALU.NOR_OP
    elif self.aluop.data == 0b11:
      if self.opcode.data == 0b001000:
        outs.alucontrol = ALU.ADD_OP
      elif self.opcode.data == 0b001010:
        outs.alucontrol = ALU.SLT_OP
      elif self.opcode.data == 0b001100:
        outs.alucontrol = ALU.AND_OP
      elif self.opcode.data == 0b001101:
        outs.alucontrol = ALU.OR_OP

class BranchControl(Component):
  inputs  = {'branch': 1, 'zero': 1, 'eq': 1}
  outputs = {'out': 1}

  def simulate(self, ins, outs):
    outs.out = self.branch.data & int(self.zero.data == self.eq.data)
