import unittest
from bitstring import BitArray

from ...components.registers import *
from ...simulator import Message, Delta

class ComponentTest(unittest.TestCase):
  def assertSimulates(self, component, ins, outs):
    for inp, val in ins.iteritems():
      getattr(component, inp).data = BitArray(val)
    actual_outs = Message()
    component.simulate(ins, actual_outs)
    self.assertEqual(actual_outs, outs)

  def ints_msg(self, **kwargs):
    for k in kwargs:
      kwargs[k] = BitArray(length = 32, int = kwargs[k])
    return Message(**kwargs)
