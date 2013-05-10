from ..components.component import *
import arch
from alu import ALU

# This is the main control unit implemented as per the diagram
# on page 24 of Lecture 5
class CPU(Component):
  delay = 200

  inputs  = {'opcode':   6}

  outputs = {'regdst':   1,
             'jump':     1,
             'branch':   1,
             'memread':  1,
             'memtoreg': 1,
             'aluop':    2,
             'memwrite': 1,
             'alusrc':   1,
             'regwrite': 1
            }

  def simulate(self, ins, outs):
    is_rtype = self.opcode.data == 0b000000
    is_lw    = self.opcode.data == 0b100011
    is_sw    = self.opcode.data == 0b101011
    is_beq   = self.opcode.data == 0b000100
    is_jmp   = self.opcode.data == 0b000010

    outs.regdst = is_rtype
    outs.jump = is_jmp
    outs.branch = is_beq
    outs.memread = is_lw
    outs.memtoreg = is_lw 
    outs.memwrite = is_sw
    outs.alusrc = is_lw | is_sw
    outs.regwrite = is_rtype | is_lw

    if is_rtype:
      outs.aluop = 0b10
    elif is_lw or is_sw:
      outs.aluop = 0b00
    elif is_beq or is_jmp:
      outs.aluop = 0b01

class ALUControl(Component):
  delay = 200

  inputs  = {'aluop':      2,
             'funct':      6}

  outputs = {'alucontrol': 4}

  def simulate(self, ins, outs):
    if self.aluop.data == 0b00:
      outs.alucontrol = ALU.ADD_OP
    elif self.aluop.data == 0b01:
      outs.alucontrol = ALU.SUB_OP
    elif self.aluop.data == 0b10:
      if self.funct.data == 0b100000:
        outs.alucontrol.data = ALU.ADD_OP
      elif self.funct.data == 0b100010:
        outs.alucontrol.data = ALU.SUB_OP
      elif self.funct.data == 0b100100:
        outs.alucontrol.data = ALU.AND_OP
      elif self.funct.data == 0b100101:
        outs.alucontrol.data = ALU.OR_OP
      elif self.funct.data == 0b101010:
        outs.alucontrol.data = ALU.SLT_OP
