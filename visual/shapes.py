# Abstract shapes with no drawing information
#
# Coordinate system:
# 0,0 at bottom left corner
# right and up are positive x and y respectively

class Shape(object):
  def __init__(self, **kwargs):
    for k, v in kwargs.iteritems():
      setattr(self, k, v)

class Quadrilatral(Shape):
  def __init__(self, width, height):
    Shape.__init__(self, width = width, height = height)

class Rectangle(Quadrilatral): pass

class Trapezium(Quadrilatral): pass

class Ellipsoid(Shape):
  def __init__(self, r1, r2):
    Shape.__init__(self, r1 = r1, r2 = r2)

class Circle(Ellipsoid):
  def __init__(self, r):
    Ellipsoid.__init__(self, r1 = r, r2 = r)

