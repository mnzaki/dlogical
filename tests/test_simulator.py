import unittest
from simulator import *
from components.misc import *
from components.registers import *

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

  def test_wires(self):
    DReg4 = DRegister.with_parameters(width = 4)
    DReg8 = DRegister.with_parameters(width = 8)

    reg1 = DReg4()
    adder = Adder32(in0 = reg1.d[:], in1 = 1)
    reg1.q = adder.out[:]
    reg2 = DReg4(q = 6)

    bigreg = DReg8(q = Wire(reg1.d[:], reg2.d[:]))
    self.assertEqual(bigreg.q.width, 8)

    sim = Simulator([Delta(100, [reg1.d, reg2.q.port])])

    # FIXME change this after fixing the lost cycle in Wire()s
    sim.step()
    sim.step()
    self.assertEqual(reg1.q.data, 1)
    self.assertEqual(reg1.d.data, 0)
    self.assertEqual(reg2.d.data, 6)
    self.assertEqual(bigreg.q.data, 0b00000110)

    # FIXME remove this after fixing the lost cycle in Wire()s
    sim.step()
    sim.step()
    self.assertEqual(reg1.q.data, 1)
    self.assertEqual(reg1.d.data, 1)
    self.assertEqual(reg2.d.data, 6)
    self.assertEqual(bigreg.q.data, 0b00010110)
