from collections import deque

from pyglet import graphics, gl

from visual.shapes import *
from components.component import Component

class CircuitRenderer(object):
  def __init__(self, arch):
    self.arch = arch
    for name, component in self.arch.__dict__.iteritems():
      if isinstance(component, Component):
        self.prepare_shape(component.shape)

  def prepare_shape(self, s):
    if isinstance(s, Rectangle):
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, s.width, 0, s.width, s.height, 0, s.height))
      )
      s.gl_type = gl.GL_QUADS
    elif isinstance(s, Trapezium):
      a = s.height / 4
      b = a * 3
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, s.width, a, s.width, b, 0, s.height))
      )
      s.gl_type = gl.GL_QUADS
    # TODO Ellipsoid
    else:
      s.vertex_list = graphics.vertex_list(4,
        ('v2i', (0, 0, 50, 0, 50, 50, 0, 50))
      )
      s.gl_type = gl.GL_QUADS

  def render_component(self, component):
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glTranslatef(component.layout.x, component.layout.y, 0.0)
    component.shape.vertex_list.draw(component.shape.gl_type)
    gl.glPopMatrix()

  def render_root(self):
    self.render_component(self.arch.root)

  def render(self):
    for name, component in self.arch.__dict__.iteritems():
      if isinstance(component, Component):
        self.render_component(component)

