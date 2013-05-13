from component import *
from visual.shapes import *

class AndGate(Component):
  delay = 10

  inputs  = {'in0': 1, 'in1': 1}
  outputs = {'out': 1}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      outs.out = self.in0.data & self.in1.data

class Mux(ParametrizedComponent):
  delay = 50
  shape = Trapezium(150, 150)

  parameters = {'width': 32}
  inputs = {'in0': 'width', 'in1': 'width', 's': 1}
  outputs = {'out': 'width'}

  # FIXME check changes?
  def simulate(self, ins, outs):
    if self.s.data == 0:
      outs.out = self.in0.data
    else:
      outs.out = self.in1.data

Mux32 = Mux.with_parameters(width = 32)

# FIXME parametrize
class Adder32(Component):
  delay = 100
  shape = Trapezium(200, 250)

  inputs = {'in0': 32, 'in1': 32}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.in0.data + self.in1.data

# FIXME parametrize
class SLL2(Component):
  delay = 50
  shape = Circle(75)

  inputs = {'inp': 32}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.inp.data << 2

class SignExt(Component):
  delay = 50
  shape = Circle(75)

  inputs = {'inp': 16}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.inp.data
