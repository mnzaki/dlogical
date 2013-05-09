import unittest
from bitstring import BitArray

from .helpers.components import *
from ..components.registers import *
from ..simulator import Message, Delta

class TestDRegister32(ComponentTest):
  def test_dregister32(self):
    dreg = DRegister32()
    ins = self.ints_msg(q = 42)
    outs = self.ints_msg(d = 42)

    self.assertSimulates(dreg, ins, outs)

class TestRegisterFile(ComponentTest):
  def setUp(self):
    self.regfile = RegisterFile.with_defaults()

  def test_reg_file(self):
    ins = self.ints_msg(write_en = 1, write_reg = 2, write = 42, read_reg1 = 1)
    outs = self.ints_msg(read1 = 0)
    self.assertSimulates(self.regfile, ins, outs)

    ins = self.ints_msg(read_reg1 = 2)
    outs = self.ints_msg(read1 = 42)
    self.assertSimulates(self.regfile, ins, outs)

  def test_write_before_read(self):
    ins = self.ints_msg(write_reg = 1, write_en = 1, write = 24, read_reg1 = 1)
    outs = self.ints_msg(read1 = 24)
    self.assertSimulates(self.regfile, ins, outs)
