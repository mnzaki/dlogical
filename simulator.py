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
    new_deltas = []
    for delta in self.deltas:
      delta.time -= self.deltas[0].time
      if delta.time == 0:
        for port in delta.ports:
          for affected in port.connections:
            new_deltas.append(affected.simulate())

    while self.deltas[0].time == 0:
      heappop(self.deltas)

    for delta in new_deltas:
      heappush(self.deltas, delta)
