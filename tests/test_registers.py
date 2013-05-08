from ..components.registers import *
import unittest
from bitstring import BitArray

class TestDRegister32(unittest.TestCase):
  def test_dregister32(self):
    dreg = DRegister32()
    dreg.q.data = BitArray('0b100010101')
    delta = dreg.simulate()
    self.assertIsInstance(delta, Delta)
    self.assertEqual(dreg.d.data, dreg.q.data)

