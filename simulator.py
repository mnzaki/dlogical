from heapq import heappush, heappop, heapify

class Message(dict):
  def __init__(self, **kwargs):
    dict.__init__(self, kwargs)
  def __getattr__(self, attr):
    return self[attr]
  def __setattr__(self, attr, val):
    self[attr] = val

class Delta:
  def __init__(self, time, ports):
    self.time = time
    self.ports = ports

  def __cmp__(self, other):
    if self.time < other.time:
      return -1
    elif self.time > other.time:
      return 1
    else:
      return 0

  def __repr__(self):
    affected = []
    for port in self.ports:
      affected.extend(port.connections)

    return "Delta(%i, %i => %s)" % (self.time, self.ports[0].data, affected)

class Simulator:
  def __init__(self, deltas = [], new_deltas_cb = None):
    heapify(deltas)
    self.deltas = deltas
    self.new_deltas_cb = new_deltas_cb

  def inject(self, inp):
    if isinstance(inp, Delta):
      heappush(self.deltas, inp)
    else:
      for delta in inp:
        heappush(self.deltas, delta)

  def step(self):
    # create a mapping of affected components to messages of affected inputs
    affected = {}
    for delta in self.deltas:
      delta.time -= self.deltas[0].time
      if delta.time == 0:
        for port in delta.ports:
          for conn in port.connections:
            if conn.component not in affected:
              affected[conn.component] = Message()
            affected[conn.component][conn.port_name] = conn.update()

    # create a list of new deltas generated as a side-effect of simulating the
    # affected components
    new_deltas = []
    for component, inputs_msg in affected.iteritems():
      outputs_msg = Message()
      delay = component.simulate(inputs_msg, outputs_msg)
      if delay is None:
        delay = component.delay

      # create the delta and update the components port data
      delta_ports = []
      for port_name, val in outputs_msg.iteritems():
        # FIXME throw exception if port could not be found
        delta_ports.append(getattr(component, port_name))
        getattr(component, port_name).data = val

      # push this delta if it is non-empty
      if len(delta_ports) != 0:
        new_deltas.append(Delta(delay, delta_ports))

    if self.new_deltas_cb:
      self.new_deltas_cb(new_deltas)

    # pop all the deltas that have been processed
    while self.deltas and self.deltas[0].time == 0:
      heappop(self.deltas)

    # push all the deltas that require processing
    for delta in new_deltas:
      heappush(self.deltas, delta)
