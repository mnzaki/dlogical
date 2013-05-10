from component import *

class AndGate(Component):
  delay = 10

  inputs  = {'in0': 1, 'in1': 1}
  outputs = {'out': 1}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      outs.out = self.in0.data & self.in1.data

class Mux(Component):
  delay = 50

  inputs = {'in0': 1, 'in1': 1, 's': 1}
  outputs = {'out': 1}

  # FIXME check changes
  def simulate(self, ins, outs):
    if self.s.data.int == 0:
      outs.out = self.ins0.data
    else:
      outs.out = self.ins1.data

# FIXME parametrize
class Adder32(Component):
  delay = 100

  inputs = {'in0': 32, 'in1': 32}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(ins) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.in0.data + self.in1.data

# FIXME parametrize
class SLL2(Component):
  delay = 50

  inputs = {'inp': 32}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(s) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.inp.data << 2

class SignExt(Component):
  delay = 50

  inputs = {'inp': 16}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(s) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = self.inp.data
