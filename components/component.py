from bitarray import bitarray

class PortConnection(object):
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

class Port(object):
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

class Component(object):
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
    inputs = self.inputs.copy()
    for port_name in kwargs:
      if port_name not in inputs:
        raise self.NoSuchInputPort(port_name)
      inputs[port_name] = kwargs[port_name]

    for port_name in inputs:
      if isinstance(inputs[port_name], int):
        inputs[port_name] = Port(inputs[port_name])()
      inputs[port_name].connect(self)
      setattr(self, port_name, inputs[port_name])

    for port_name in self.outputs:
      setattr(self, port_name, Port(self.outputs[port_name]))

  def simulate(self):
    raise NotImplementedError

class ParametrizedComponent(Component):
  parameters = {
#    'width1' : some_width
  }

  class ParameterMissing(Exception): pass

  @classmethod
  def with_parameters(klass, **kwargs):
    name = klass.__name__ + "_" + "_".join(map(str, kwargs.values()))
    inputs, outputs = klass.inputs.copy(), klass.outputs.copy()
    params = klass.parameters.copy()
    params.update(kwargs)

    for d in [inputs, outputs]:
      for k in d:
        if isinstance(d[k], str):
          try: d[k] = params[d[k]]
          except KeyError: raise klass.ParameterMissing(d[k])

    return type(name, (klass,), dict(inputs = inputs, outputs = outputs))
