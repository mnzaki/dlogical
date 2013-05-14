from heapq import heappush, heappop, heapify
from utils import Bunch

class Message(Bunch): pass

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
    s = "Delta(%i, " % self.time
    for port, val in self.ports:
      s += "%i => %s, " % (val, port.connections)
    s += ")"
    return s

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

  def trigger_component(self, comp):
    delta_ports = []
    for port_conn in comp.inputs.values():
      delta_ports.append((port_conn.port, port_conn.data))
    self.inject(Delta(0, delta_ports))

  def trigger_root(self, arch):
    self.trigger_component(arch.root)

  def step(self):
    # create a mapping of affected components to messages of affected inputs
    affected = {}
    delta_time = self.deltas[0].time
    for delta in self.deltas:
      delta.time -= delta_time
      if delta.time == 0:
        for port, val in delta.ports:
          if not hasattr(port, 'simulated_at_least_once') or port.data != val:
            port.simulated_at_least_once = True
            port.data = val
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
        port = getattr(component, port_name)
        delta_ports.append((port, val))

      # push this delta if it is non-empty
      if len(delta_ports) != 0:
        new_deltas.append(Delta(delay, delta_ports))

    # pop all the deltas that have been processed
    while self.deltas and self.deltas[0].time == 0:
      heappop(self.deltas)

    # push all the deltas that require processing
    for delta in new_deltas:
      heappush(self.deltas, delta)

    if self.new_deltas_cb:
      self.new_deltas_cb(self, affected, new_deltas)

    return delta_time
