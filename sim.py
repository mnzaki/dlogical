#!/usr/bin/env python2

from mips import MIPSArchitecture
from mips.asm import Assembler
from simulator import *
from components.component import *
import sys
import readline
from bitstring import BitArray

MAX_ADVANCE_STEPS = 100

assembler = Assembler()
asm = list(assembler.assemble(sys.argv[1]))

mips = MIPSArchitecture()

for i, a in enumerate(asm):
  mips.imem.mem[i] = a

col_width = 30 
def print_deltas(deltas):
  deltas.sort()
  for d in deltas:
    print d

def change_cb(sim, affected, deltas):
  #print_deltas(deltas)
  print
  for comp, ports in affected.iteritems():
    s = "%s" % comp
    print comp, " " * (col_width - len(s)),
    for port, val in ports.iteritems():
      print "%s = %i," % (port, val),
    print
  print

sim = Simulator()
sim.trigger_root(mips)
sim.new_deltas_cb = change_cb

print "Beginning Simulation"
print "Initial Delta Set: ", sim.deltas
print "Commands: 'q[uit]' to quit'"
print "          'd[eltas]' for the current delta set"
print "          'i[nspect] <memaddr>' to inspect memory at address <memaddr>"
print "          'r[egister] <regnum>' to inspect value of register number <regnum>"
print "          'p[ort] comp.port|comp' to inspect value of a port"
print "          'a[dvance] <expr>' advance the simulation until <expr> is true"
print "          's[kip] <time>' skip at least <time> time units"
print "          'm[em] <offset>'"
print "Press Enter to advance the simulation"
print

while True:
  try:
    inp = raw_input(">>> ")
  except EOFError, KeyboardInterrupt:
    break
  if inp:
    try:
      inp = inp.split(" ", 1)
      cmd = inp[0]
      if len(inp) > 1:
        inp = inp[1]
      else:
        inp = None
      if cmd == 'q' or cmd == "quit":
        break
      elif cmd == 'd' or cmd == 'deltas':
        print_deltas(list(sim.deltas))
      elif cmd == 'i' or cmd == 'inspect':
        addr = eval(inp)
        print mips.imem.mem[addr / 4]
      elif cmd == 'r' or cmd == 'register':
        reg = int(inp)
        b = BitArray(length = 32, uint = mips.regs.registers[reg])
        print b.int
      elif cmd == 'p' or cmd == 'port':
        port = "mips." + inp
        obj = eval(port)
        if isinstance(obj, Port) or isinstance(obj, PortConnection):
          obj = obj.data
        print obj
      elif cmd == 'a' or cmd == 'advance':
        if not inp: raise Exception("You must provide an expression!")
        max_steps = MAX_ADVANCE_STEPS
        while True:
          max_steps -= 1
          sim.step()
          print
          if max_steps < 0:
             raise Exception("Maximum number of steps (%i) taken"\
                             " and expression '%s' is still not true"\
                             % (MAX_ADVANCE_STEPS, inp))
          if eval(inp, mips.__dict__):
            break
      elif cmd == 's' or cmd == 'skip':
        to_skip = int(inp)
        while to_skip > 0:
          to_skip -= sim.step()
        print
        print "Skipped ahead %i" % (int(inp) - to_skip)
      elif cmd == 'm' or cmd == 'mem':
        inp = int(inp)
        print mips.dmem.mem[inp]
      else:
        raise Exception("Invalid command")
    except Exception as e:
      print e
  else:
    sim.step()
  print

print "It was a pleasure simulating for you"
