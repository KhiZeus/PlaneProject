class Fuselage:
  def __init__(self, volume, mass, section_surface, length):
    self.volume = volume
    self.mass = mass
    self.section_surface = section_surface
    self.length = length

  def get_volume(self):
    return self.volume

  def get_mass(self):
    return self.mass

  def get_section_surface(self):
    return self.section_surface

  def get_length(self):
    return self.length