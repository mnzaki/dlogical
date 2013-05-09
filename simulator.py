from heapq import heappush, heappop
from bitstring import BitArray

class Message(dict):
  def __init__(self, **kwargs):
    dict.__init__(self, kwargs)
    self.__dict__ = self

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

class Simulator:
  def __init__(self):
    self.deltas = []

  def step(self):
    # create a mapping of affected components to messages of affected inputs
    affected = {}
    for delta in self.deltas:
      delta.time -= self.deltas[0].time
      if delta.time == 0:
        for port in delta.ports:
          for connection in port.connections:
            if conn.component not in affected:
              affected[conn.component] = Message()
            affected[conn.component][conn.port_name] = BitArray(port.data)

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
        setattr(component, port_name, BitArray(val))

      # push this delta if it is non-empty
      if len(delta_ports) != 0:
        new_deltas.append(Delta(delay, delta_ports))

    # pop all the deltas that have been processed
    while self.deltas[0].time == 0:
      heappop(self.deltas)

    # push all the deltas that require processing
    for delta in new_deltas:
      heappush(self.deltas, delta)
