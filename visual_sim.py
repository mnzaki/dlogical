#!/usr/bin/env python2

from simulator import *
from gui.circuit_drawing_area import *
from gui.circuit_renderer import *

# FIXME load arch and layout based on name from argv
import mips
arch = mips.MIPSArchitecture()
layout = mips.layout.MIPSColumnLayout(arch)

def new_deltas_cb(sim, affected, deltas):
  print deltas

sim = Simulator()
sim.new_deltas_cb = new_deltas_cb
sim.trigger_root(arch)

sim.step()

renderer = CircuitRenderer(arch)

mw = gtk.Window()
mw.connect('destroy', gtk.main_quit)
darea = CircuitDrawingArea(renderer)
darea.set_size_request(700, 700)
vbox = gtk.VBox()
vbox.set_homogeneous(0)
mw.add(vbox)
b = gtk.Button('Upper')
vbox.pack_start(b, 0, 0)
vbox.pack_start(darea, 1, 1)
b = gtk.Button('Lower')
vbox.pack_end(b, 0, 0)
mw.show_all()

gtk.main()
