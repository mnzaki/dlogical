import unittest
from ..simulator import *
from ..components.misc import *
from ..components.registers import *

class TestSimulator(unittest.TestCase):
  def test_simple_counter(self):
    reg = DRegister32()
    adder = Adder32(in0 = reg.d[:], in1 = 1)
    reg.q = adder.out[:]

    sim = Simulator()
    sim.inject(Delta(100, [reg.d]))

    sim.step()
    self.assertEqual(len(sim.deltas), 1)
    self.assertEqual(sim.deltas[0].ports[0], adder.out)
    self.assertEqual(adder.out.data, 1)
    self.assertEqual(reg.q.data, 1)
    self.assertEqual(reg.d.data, 0)

    sim.step()
    self.assertEqual(len(sim.deltas), 1)
    self.assertEqual(sim.deltas[0].ports[0], reg.d)
    self.assertEqual(adder.out.data, 1)
    self.assertEqual(reg.q.data, 1)
    self.assertEqual(reg.d.data, 1)
