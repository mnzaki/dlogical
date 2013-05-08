import unittest
from ..components.component import *

class SomeComponent(Component):
  inputs = {'in1': 8, 'in2': 4}
  outputs = {'out1': 1, 'out2': 4}

class TestComponentClass(unittest.TestCase):
  def setUp(self):
    self.t1 = SomeComponent()

  def test_nonexistent_input(self):
    self.assertRaises(Component.NoSuchInputPort, SomeComponent, nonexistent = self.t1.out1())

  def test_component_creation(self):
    self.assertTrue(hasattr(self.t1, 'out1'))
    self.assertTrue(hasattr(self.t1, 'out2'))

    t2 = SomeComponent(in1 = self.t1.out1(), in2 = self.t1.out2())
    self.assertTrue(hasattr(t2, 'in1'))
    self.assertTrue(hasattr(t2, 'in2'))

  def test_unconnected_input(self):
    self.assertTrue(hasattr(self.t1, 'in1'))
    self.assertEqual(int(self.t1.in1.data.to01(), 2), 0)
