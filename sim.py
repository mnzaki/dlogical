#!/usr/bin/env python2

from mips import MIPSArchitecture
from mips.asm import Assembler
from simulator import *
import sys

assembler = Assembler()
asm = list(assembler.assemble(sys.argv[1]))

mips = MIPSArchitecture()

for i, a in enumerate(asm):
  mips.imem.mem[i] = a

col_width = 30 
def change_cb(sim, affected, deltas):
  #print sim.deltas
  for comp, ports in affected.iteritems():
    s = "%s" % comp
    print comp, " " * (col_width - len(s)),
    for port, val in ports.iteritems():
      print "%s = %i," % (port, val),
    print


sim = Simulator()
sim.trigger_root(mips)
sim.new_deltas_cb = change_cb

print "Beginning Simulation"
print "Initial Delta Set: ", sim.deltas
print "Commands: 'd[eltas]' for the current delta set, 'q[uit]' to quit"
print "Press Enter to advance the simulation"
print

while True:
  try:
    inp = raw_input(">>> ")
  except EOFError, KeyboardInterrupt:
    break
  if inp:
    if inp[0] == 'q':
      break
    elif inp[0] == 'd':
      deltas = list(sim.deltas)
      deltas.sort()
      for d in deltas:
        print d
  else:
    sim.step()
  print

print "It was a pleasure simulating for you"
