from ..components.registers import *
import unittest
from bitarray import bitarray

class TestDReg(unittest.TestCase):
  def test_dreg(self):
    dreg = DRegister()
    dreg.q.data = bitarray('100010101')
    delta = dreg.simulate()
    assertIsInstance(delta, Delta.type)
    assertEqual(dreg.d.data, dreg.q.data)

