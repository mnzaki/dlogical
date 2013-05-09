from ..components.registers import *
from ..simulator import Message, Delta

import unittest
from bitstring import BitArray

class TestDRegister32(unittest.TestCase):
  def test_dregister32(self):
    dreg = DRegister32()
    ins = Message(q = BitArray(length = 10, int = 42))
    outs = Message()
    dreg.simulate(ins, outs)
    self.assertTrue(hasattr(outs, 'd'))
    self.assertEqual(outs.d.int, 42)

