class Engine:
  def __init__(self, thrust, consumption):
    self.thrust = thrust
    self.consumption = consumption

  def get_thrust(self):
    return self.thrust

  def get_consumption(self):
    return self.consumption