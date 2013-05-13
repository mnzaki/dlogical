from components.component import *

# This works by triggering itself after every delay unit
# FIXME this is broken. It needs to trigger itself at delay/2 first to create a
# proper clock signal
class Oscillator(ParametrizedComponent):
  parameters = {'freq': 250}
  inputs = {'self_trigger': 1}
  outputs = {'clk': 1}

  def __init__(self, **kwargs):
    Component.__init__(self, **kwargs)
    # probably need to use setattr or it will affect the entire class
    setattr(self, 'delay', self.parameters['freq'] / 2)
    self.self_trigger = self.clk[:]

  def simulate(self, ins, outs):
    if ins.self_trigger == 1:
      outs.clk = 0
    else:
      outs.clk = 1
