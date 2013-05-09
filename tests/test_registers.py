import unittest

from .helpers.components import *
from ..components.registers import *
from ..simulator import Message, Delta

class TestDRegister32(ComponentTest):
  def test_dregister32(self):
    dreg = DRegister32()
    ins = Message(q = 42)
    outs = Message(d = 42)

    self.assertSimulates(dreg, ins, outs)

class TestRegisterFile(ComponentTest):
  def setUp(self):
    self.regfile = RegisterFile.with_defaults()

  def test_reg_file(self):
    ins = Message(write_en = 1, write_reg = 2, write = 42, read_reg1 = 1)
    outs = Message(read1 = 0)
    self.assertSimulates(self.regfile, ins, outs)

    ins = Message(read_reg1 = 2)
    outs = Message(read1 = 42)
    self.assertSimulates(self.regfile, ins, outs)

  def test_write_before_read(self):
    ins = Message(write_reg = 1, write_en = 1, write = 24, read_reg1 = 1)
    outs = Message(read1 = 24)
    self.assertSimulates(self.regfile, ins, outs)
