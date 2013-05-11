import imp
import os
from components.component import Component

class Architecture(object):
  module_name = ''
  root = ''
  def __init__(self):
    module_name = os.path.join(*self.module_name.split('.'))
    mod_info = imp.find_module(module_name)
    module = imp.load_module(module_name, *mod_info)
    for k, v in module.__dict__.iteritems():
      if isinstance(v, Component):
        v.name = k
        setattr(self, k, v)
        if k == self.root:
          self.root = v

def new_architecture(name, module_name, root):
  return type("%sArchitecture" % name, (Architecture,),
              dict(module_name = module_name, root = root))
