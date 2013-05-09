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
    self.assertEqual(self.t1.in1.data, 0)


class SomeParametrizedComponent(ParametrizedComponent):
  parameters = {'width': 8, 'width_out': 16}
  inputs = {'in1' : 'width', 'in2': 'width_2'}
  outputs = {'out1' : 'width_out'}

  @classmethod
  def process_parameters(klass, params):
    params['width_2'] = params['width'] / 2

class TestParametrizedComponents(unittest.TestCase):
  def test_setting(self):
    klass = SomeParametrizedComponent.with_parameters(width = 16, width_out = 8)
    inst = klass()
    self.assertTrue(hasattr(inst, 'in1'))
    self.assertTrue(hasattr(inst, 'in2'))
    self.assertTrue(hasattr(inst, 'out1'))

    self.assertEqual(klass.inputs['in1'], 16)
    self.assertEqual(klass.inputs['in2'], 8)
    self.assertEqual(klass.outputs['out1'], 8)

  def test_using_some_defaults(self):
    klass = SomeParametrizedComponent.with_parameters(width_out = 4)
    inst = klass()
    self.assertTrue(hasattr(inst, 'in1'))
    self.assertTrue(hasattr(inst, 'in2'))
    self.assertTrue(hasattr(inst, 'out1'))
    self.assertEqual(klass.inputs['in1'], 8)
    self.assertEqual(klass.inputs['in2'], 4)
    self.assertEqual(klass.outputs['out1'], 4)

  def test_using_defaults(self):
    inst = SomeParametrizedComponent.with_defaults()
    self.assertTrue(hasattr(inst, 'in1'))
    self.assertTrue(hasattr(inst, 'in2'))
    self.assertTrue(hasattr(inst, 'out1'))

  def test_direct_instantiation(self):
    self.assertRaises(ParametrizedComponent.AbstractComponent, SomeParametrizedComponent)
