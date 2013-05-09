from heapq import heappush

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
    # create a mapping of affected components to array of affected ports
    affected = {}
    for delta in self.deltas:
      delta.time -= self.deltas[0].time
      if delta.time == 0:
        for port in delta.ports:
          for connection in port.connections:
            if conn.component not in affected:
              affected[conn.component] = []
            affected[conn.component].append(conn.port_name)

    new_deltas = []
    for component, port_names in affected.iteritems():
      deltas = component.simulate(port_names)
      if deltas is not None and len(deltas) != 0:
        new_deltas.append(deltas)

    while self.deltas[0].time == 0:
      heappop(self.deltas)

    for delta in new_deltas:
      heappush(self.deltas, delta)
