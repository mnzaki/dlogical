from ..simulator import Delta

class PortConnection(object):
  def __init__(self, port, start, end):
    self.port = port
    self.start = start
    self.end = end
    self.mask = ~(~0 << (self.start + 1))
    self.width = start - end + 1
    self.update()

  def connect(self, component, port_name):
    self.component = component
    self.port_name = port_name
    self.port.connections.append(self)

  def update(self):
    if self.width == self.port.width:
      self.data = self.port.data
    else:
      self.data = (self.port.data & self.mask) >> self.end
    return self.data

class Port(object):
  class InvalidPortSlice(Exception): pass

  def __init__(self, width, data = 0):
    self.connections = []
    self.width = width
    self.width_mask = ~(~0 << width)
    self.data = data

  # A port is 'sliced' as part of input assignement for a component
  def __getitem__(self, key):
    if isinstance(key, slice):
      if key.step is not None:
        raise self.InvalidPortSlice("Ports cannot be accessed with step arguments!")
      start = key.start or (self.width - 1)
      end = key.stop or 0
    elif isinstance(key, int):
      start = key
      end = key
    else:
      raise self.InvalidPortSlice("Ports can either be accessed with slices or indices!")

    return PortConnection(self, start, end)

  def __setattr__(self, name, value):
    if name == 'data':
      value &= self.width_mask
    object.__setattr__(self, name, value)
    if name == 'data':
      for conn in self.connections:
        conn.update()

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
  class InvalidPortConnection(Exception): pass

  def __init__(self, **kwargs):
    inputs = self.inputs.copy()
    for port_name in kwargs:
      try: inputs.pop(port_name)
      except KeyError: raise self.NoSuchInputPort(port_name)
      setattr(self, port_name, kwargs[port_name])

    for port_name in inputs:
      setattr(self, port_name, 0)

    self.output_ports = []
    for port_name in self.outputs:
      port = Port(self.outputs[port_name])
      setattr(self, port_name, port)
      self.output_ports.append(port)

  def __setattr__(self, name, value):
    if name in self.inputs:
      if isinstance(value, int):
        # create a dummy port simply to hold this value
        value = Port(self.inputs[name], value)[:]
      if not isinstance(value, PortConnection):
        raise self.InvalidPortConnection(value)
      value.connect(self, name)

    if name in self.outputs and hasattr(self, name):
      raise self.InvalidPortConnection("You cannot change an output port of a component!")

    super(Component, self).__setattr__(name, value)

  def simulate(self, ports):
    raise NotImplementedError

  def changed(self, *args):
    if len(args) == 0:
      return None
    else:
      return Delta(self.delay, args)

# FIXME this feels like such a hack
# Usage is supposed to be like a normal PortConnection for Component inputs
class Wire(PortConnection):
  delay = 0

  def __init__(self, *args):
    self.width = 0
    for pos, arg in enumerate(args):
      # FIXME support a mix of connections and constant values
      if not isinstance(arg, PortConnection):
        raise Exception("A wire must consist of PortConnections!")
      self.width += arg.width
      arg.connect(self, "conn%i" % pos)

    self.inputs = list(args)
    self.port = Port(self.width)
    self.update()

  def update(self):
    width = self.width
    self.data = 0
    for conn in self.inputs:
      width -= conn.width
      self.data |= conn.data << width
    return self.data

  def simulate(self, ins, outs):
    outs.port = self.update()

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

    # FIXME I don't like this; this needs a rewrite/redesign
    # skip ParametrizedComponent's init, but still allow subclasses to have an init
    init = klass.__init__
    if init == ParametrizedComponent.__init__:
      init = Component.__init__
    new_klass = type(name, (klass,), dict(__init__ = init, inputs = inputs, outputs = outputs))
    new_klass.parameters = params

    return new_klass

  @classmethod
  def with_defaults(klass, **kwargs):
    if not hasattr(klass, 'default_class'):
      klass.default_class = klass.with_parameters()
    return klass.default_class(**kwargs)
