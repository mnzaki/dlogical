from components.component import Component
from utils import Bunch
from collections import deque

class Layout(Bunch): pass

class LayoutManager(object):
  def __init__(self, arch):
    pass

class ColumnLayoutManager(LayoutManager):
  class Layout(Layout): pass

  def __init__(self, arch):
    super(ColumnLayoutManager, self).__init__(arch)

    column = 0
    components = deque([arch.root])
    while components:
      elem = components.popleft()
      # FIXME adjust column width depending on widest component
      # FIXME distribute components along the y axis
      elem.layout = self.Layout(column = column, x = column * 200, y = 100)
      if not isinstance(elem, Component): continue
      for port in elem.output_ports:
        for conn in port.connections:
          if not hasattr(conn.component, 'layout'):
            components.append(conn.component)
      column += 1

