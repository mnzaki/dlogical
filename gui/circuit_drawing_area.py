from collections import deque
import gtk, gobject
import pyglet
from pyglet import gl

from gtk_pyglet_drawing_area import GtkGlDrawingArea

class CircuitDrawingArea(GtkGlDrawingArea):
  def __init__(self, renderer):
    super(CircuitDrawingArea, self).__init__()
    self.renderer = renderer
    self.trans = [0, 0, 1]

    self.connect('motion_notify_event', self.on_motion_notify)
    self.connect('button_press_event', self.on_button_press)
    self.connect('scroll-event', self.on_mouse_scroll)

    self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.SCROLL_MASK)

    self.renderer.render()

  def on_button_press(self, widget, event):
    self.old_x, self.old_y = event.x, event.y
    return True

  def on_motion_notify(self, widget, event):
    if event.is_hint:
      x, y, state = event.window.get_pointer()
    else:
      x = event.x
      y = event.y
      state = event.state

    if not (state & (gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON2_MASK |
             gtk.gdk.BUTTON3_MASK)):
      return True

    dx = self.old_x - x
    dy = self.old_y - y
    self.old_x, self.old_y = x, y

    self.trans[0] -= dx
    self.trans[1] += dy

    self.queue_draw()
    return True

  def on_mouse_scroll(self, widget, event):
    # FIXME zoom centered on mouse instead
    if event.direction == gtk.gdk.SCROLL_UP:
      self.trans[2] *= 1.2
    elif event.direction == gtk.gdk.SCROLL_DOWN:
      self.trans[2] *= 0.8
    self.queue_draw()

  def setup(self):
    # One-time GL setup
    gl.glClearColor(1, 1, 1, 0)
    gl.glColor3f(1, 0, 0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glDisable(gl.GL_LIGHTING)

  def display(self, width, height):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.glTranslatef(self.trans[0], self.trans[1], 0)
    gl.glScalef(self.trans[2], self.trans[2], self.trans[2])
    # FIXME draw only visible part?
    self.renderer.render()
