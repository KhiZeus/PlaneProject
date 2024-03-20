class Engine:
    """
  A class representing an engine with its thrust and fuel consumption.
  """

    def __init__(self, thrust, consumption):
        """
    Initialize the Engine object.

    Parameters:
    - thrust (float): The thrust of the engine.
    - consumption (float): The fuel consumption of the engine.
    """
        self.thrust = thrust
        self.consumption = consumption

    def get_thrust(self):
        """
    Get the thrust of the engine.

    Returns:
    - thrust (float): The thrust of the engine.
    """
        return self.thrust

    def get_consumption(self):
        """
    Get the fuel consumption of the engine.

    Returns:
    - consumption (float): The fuel consumption of the engine.
    """
        return self.consumption


def convert_consumption_to_TSFC(CBHP, speed, propeller_efficiency):
    """
  Convert CBHP (brake horsepower fuel consumption) to TSFC (thrust specific fuel consumption).

  Parameters:
  - CBHP (float): Brake horsepower fuel consumption in lb/hr/brake horsepower.
  - Vit (float): Flight speed in ft/s.
  - eff (float): Propeller efficiency.

  Returns:
  - TSFC (float): Thrust specific fuel consumption in lb/hr/lb.
  """
    # Conversion
    TSFC = CBHP * speed / (550 * propeller_efficiency)
    return TSFC


# Example usage
CBHP = 0.45  # lb/hr/brake horsepower
Vit = 100  # ft/s
eff = 0.75  # Propeller efficiency

TSFC = convert_consumption_to_TSFC(CBHP, Vit, eff)
print("TSFC:", TSFC, "lb/hr/lb")
