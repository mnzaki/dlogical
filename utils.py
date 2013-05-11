class Bunch(dict):
  def __init__(self, **kwargs):
    dict.__init__(self, kwargs)
  def __getattr__(self, attr):
    return self[attr]
  def __setattr__(self, attr, val):
    self[attr] = val

