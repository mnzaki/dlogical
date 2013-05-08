from ..components.registers import *
import unittest
from bitarray import bitarray

class TestDRegister32(unittest.TestCase):
  def test_dregister32(self):
    dreg = DRegister32()
    dreg.q.data = bitarray('100010101')
    delta = dreg.simulate()
    self.assertIsInstance(delta, Delta)
    self.assertEqual(dreg.d.data, dreg.q.data)

