__all__ = ['arch', 'asm', 'control', 'alu']

import arch
from components.component import Component

for k, v in arch.__dict__.iteritems():
  if isinstance(v, Component):
    v.name = k
