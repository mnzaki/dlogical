import unittest

from simulator import Message, Delta

class ComponentTest(unittest.TestCase):
  def assertSimulates(self, component, ins, outs):
    for inp, val in ins.iteritems():
      getattr(component, inp).data = val
    actual_outs = Message()
    component.simulate(ins, actual_outs)
    self.assertEqual(actual_outs, outs)
