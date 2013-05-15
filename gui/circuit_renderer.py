from collections import deque

from pyglet import graphics, gl

from visual.shapes import *
from components.component import *

class CircuitRenderer(object):
  def __init__(self, arch):
    self.arch = arch
    # FIXME make this more efficient than 2n
    for name, component in self.arch.__dict__.iteritems():
      if isinstance(component, Component):
        self.prepare_component(component)
    for name, component in self.arch.__dict__.iteritems():
      if isinstance(component, Component):
        self.prepare_wires(component)

  def prepare_component(self, component):
    in_start = in_end = out_start = out_end = 0
    out_x = 0
    s = component.shape
    if isinstance(s, Rectangle):
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, s.width, 0, s.width, s.height, 0, s.height))
      )
      s.gl_type = gl.GL_QUADS
      in_end = out_end = s.height
      out_x = s.width
    elif isinstance(s, Trapezium):
      a = s.height / 4
      b = a * 3
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, s.width, a, s.width, b, 0, s.height))
      )
      s.gl_type = gl.GL_QUADS
      in_end = s.height
      out_start = a
      out_end = b
      out_x = s.width
    # TODO Ellipsoid
    else:
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, 50, 0, 50, 50, 0, 50))
      )
      s.gl_type = gl.GL_QUADS
      in_end = out_end = 50
      out_x = 50

    component.layout.in_spacing = (in_end - in_start) / (len(component.inputs) + 1)
    component.layout.out_spacing = (out_end - out_start) / (len(component.outputs) + 1)
    component.layout.out_x_offset = out_x

    i = 1 # input port connection index
    for port_name, port_conn in component.inputs.iteritems():
      if isinstance(port_conn, Wire):
        self.prepare_component(port_conn)
      port_conn.layout_index = i
      i += 1

  def prepare_wires(self, component):
    s = component.shape
    vlist = []
    i = 1 # output port index
    for port_name, port in component.outputs.iteritems():
      for port_conn in port.connections:
        dx = port_conn.component.layout.x - component.layout.x
        dy = port_conn.component.layout.y - component.layout.y +\
             port_conn.layout_index * port_conn.component.layout.in_spacing
        y0 = i * component.layout.out_spacing
        x0 = component.layout.out_x_offset
        vlist.extend([x0, y0, dx/2, y0, dx/2, dy, dx, dy])
      i += 1
    s.wire_vertex_list = graphics.vertex_list(len(vlist)/2,
      ('v2i', vlist)
    )
    
  def render_component(self, component):
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glTranslatef(component.layout.x, component.layout.y, 0.0)
    component.shape.vertex_list.draw(component.shape.gl_type)
    component.shape.wire_vertex_list.draw(gl.GL_LINES)
    gl.glPopMatrix()

  def render_root(self):
    self.render_component(self.arch.root)

  def render(self):
    for name, component in self.arch.__dict__.iteritems():
      if isinstance(component, Component):
        self.render_component(component)

