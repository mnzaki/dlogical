from components.component import Component
from utils import Bunch
from collections import deque

class Layout(Bunch): pass

class LayoutManager(object):
  def __init__(self, arch):
    pass

class ColumnLayoutManager(LayoutManager):
  class Layout(Layout): pass

  def __init__(self, arch, root = None):
    super(ColumnLayoutManager, self).__init__(arch)

    if root is None:
      for k, v in arch.__dict__.iteritems():
        if isinstance(v, Component):
          root = v
          break

    column = 0
    components = deque([root])
    while components:
      elem = components.popleft()
      elem.layout = self.Layout(column = column)
      if not isinstance(elem, Component): continue
      for port in elem.output_ports:
        for conn in port.connections:
          if not hasattr(conn.component, 'layout'):
            components.append(conn.component)
      column += 1

