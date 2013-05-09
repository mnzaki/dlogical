from component import *
from bitstring import BitArray

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
    if len(s) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = BitArray(length = 32, self.in0.data.int + self.in1.data.int)

# FIXME parametrize
class SLL2(Component):
  delay = 50

  inputs = {'in': 32}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(s) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = BitArray(length = 32, self.in.data.uint << 2)

class SignExt(Component):
  delay = 50

  inputs = {'in': 16}
  outputs = {'out': 32}

  def simulate(self, ins, outs):
    if len(s) > 0:
      # FIXME normalize messages: auto convert ints to bitarrays
      outs.out = BitArray(length = 32, self.in.data.uint)
