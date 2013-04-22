from bitarray import bitarray

class PortConnection:
  def __init__(self, port, start, end):
    self.port = port
    self.start = start
    self.end = end
    if start is not None and end is not None:
      self.width = start - end + 1
    else:
      self.width = self.port.width
    self.data = port.data

  def connect(self, component):
    self.port.connections.append(component)

class Port:
  def __init__(self, width, data = None):
    self.connections = []
    self.width = width
    if data is not None:
      self.data = bitarray(data)
    else:
      self.data = bitarray('0' * width)

  # A port is 'called' as part of input assignement for a component
  def __call__(self, start = None, end = None):
    return PortConnection(self, start, end)

class Component:
  outputs = {
#   'output1': output_width
  }

  inputs = {
#   'input1': input_width
  }

  # delay in ms
  delay = 42

  class NoSuchPort(Exception): pass
  class NoSuchInputPort(NoSuchPort): pass
  class NoSuchOutputPort(NoSuchPort): pass

  def __init__(self, **kwargs):
    for port_name in kwargs:
      if port_name not in self.inputs:
        raise self.NoSuchInputPort(port_name)
      port_conn = kwargs[port_name]
      port_conn.connect(self)
      setattr(self, port_name, port_conn)

    for port_name in self.outputs:
      setattr(self, port_name, Port(self.outputs[port_name]))

  def simulate(self):
    raise NotImplementedError
