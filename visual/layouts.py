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
    next_components = deque()
    while components:
      elem = components.popleft()
      print elem
      if not isinstance(elem, Component): continue
      elem.layout = self.layout(column)
      for port in elem.outputs.values():
        for conn in port.connections:
          if conn.component is not arch.root and\
             conn.component not in next_components:
            if hasattr(conn.component, 'layout') and\
               hasattr(conn.component.layout, 'relayout'):
              conn.component.layout.relayout -= 1
              print conn.component.layout
              if conn.component.layout.relayout < 0:
                next
            next_components.append(conn.component)
      if not components:
        print "NEEEEEEEEEEEEXT"
        print
        components, next_components = next_components, components
        column += 1

  def layout(self, column):
    # FIXME adjust column width depending on widest component
    # FIXME distribute components along the y axis
    return self.Layout(column = column, x = column * 200, y = 100)
