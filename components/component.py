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
  class AbstractComponent(Exception): pass

  def __init__(self, **kwargs):
    raise self.AbstractComponent(
      "You can't instantiate this directly! " +
      "Use %s.with_defaults(port1 = conn1....) instead" % self.__class__.__name__
    )

  @classmethod
  def process_parameters(klass, params): pass

  @classmethod
  def with_parameters(klass, **kwargs):
    inputs, outputs = klass.inputs.copy(), klass.outputs.copy()
    params = klass.parameters.copy()
    params.update(kwargs)
    klass.process_parameters(params)
    name = klass.__name__ + "_" + "_".join(map(str, params.values()))

    for d in [inputs, outputs]:
      for k in d:
        if isinstance(d[k], str):
          try: d[k] = params[d[k]]
          except KeyError: raise klass.ParameterMissing(d[k])

    # FIXME I don't like this
    new_klass = type(name, (klass,), dict(__init__ = Component.__init__, inputs = inputs, outputs = outputs))
    new_klass.parameters = params

    return new_klass

  @classmethod
  def with_defaults(klass, **kwargs):
    if not hasattr(klass, 'default_class'):
      klass.default_class = klass.with_parameters()
    return klass.default_class(**kwargs)
