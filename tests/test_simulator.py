import unittest
from simulator import *
from components.misc import *
from components.registers import *

class TestSimulator(unittest.TestCase):
  def setUp(self):
    def new_deltas_cb(sim, affected, deltas):
      print deltas
      print
      print affected
      print
    self.sim = Simulator()
    self.sim.new_deltas_cb = new_deltas_cb

  def test_simple_counter(self):
    self.sim.deltas = []
    reg = DRegister32()
    adder = Adder32(in0 = reg.d[:], in1 = 1)
    reg.q = adder.out[:]

    self.sim.trigger_component(reg)

    self.sim.step()
    self.assertEqual(len(self.sim.deltas), 1)
    self.assertEqual(self.sim.deltas[0].ports[0], (reg.d, 0))

    self.sim.step()
    self.assertEqual(len(self.sim.deltas), 1)
    self.assertEqual(self.sim.deltas[0].ports[0], (adder.out, 1))
    self.assertEqual(adder.out.data, 0)
    self.assertEqual(reg.q.data, 0)
    self.assertEqual(reg.d.data, 0)

    self.sim.step()
    self.assertEqual(len(self.sim.deltas), 1)
    self.assertEqual(self.sim.deltas[0].ports[0], (reg.d, 1))
    self.assertEqual(adder.out.data, 1)
    self.assertEqual(reg.q.data, 1)
    self.assertEqual(reg.d.data, 0)

    self.sim.step()
    self.assertEqual(len(self.sim.deltas), 1)
    self.assertEqual(self.sim.deltas[0].ports[0], (adder.out, 2))
    self.assertEqual(adder.out.data, 1)
    self.assertEqual(reg.q.data, 1)
    self.assertEqual(reg.d.data, 1)

  def test_wires(self):
    self.sim.deltas = []
    DReg4 = DRegister.with_parameters(width = 4)
    DReg8 = DRegister.with_parameters(width = 8)

    reg1 = DReg4()
    adder = Adder32(in0 = reg1.d[:], in1 = 1)
    reg1.q = adder.out[:]
    reg2 = DReg4(q = 6)

    bigreg = DReg8(q = Wire(reg1.d[:], reg2.d[:]))
    self.assertEqual(bigreg.q.width, 8)

    self.sim.trigger_component(reg1)
    self.sim.trigger_component(reg2)
    self.sim.step()
    self.sim.step()

    # FIXME change this after fixing the lost cycle in Wire()s
    self.sim.step()
    self.sim.step()
    self.assertEqual(reg1.q.data, 1)
    self.assertEqual(reg1.d.data, 0)
    self.assertEqual(reg2.d.data, 6)
    self.assertEqual(bigreg.q.data, 0b00000110)

    # FIXME remove this after fixing the lost cycle in Wire()s
    self.sim.step()
    self.sim.step()
    self.assertEqual(reg1.q.data, 1)
    self.assertEqual(reg1.d.data, 1)
    self.assertEqual(reg2.d.data, 6)
    self.assertEqual(bigreg.q.data, 0b00010110)
