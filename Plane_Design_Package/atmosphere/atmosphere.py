import math
from Plane_Design_Package.constants import Constants

class Atmosphere:
    """Class representing atmospheric properties at a given altitude."""

    def __init__(self, altitude=0):
        """
        Initialize Atmosphere object.

        Args:
            altitude (float): Altitude in meters. Default is 0.

        Attributes:
            q (float): Gravitational constant.
            altitude (float): Altitude in meters.
            temperature_K (float): Temperature in Kelvin.
            temperature_C (float): Temperature in Celsius.
            pressure (float): Pressure in Pascal.
            density (float): Density in kg/m^3.
            gravity (float): Gravity at altitude in m/s^2.
        """
        self.altitude = altitude  # meters
        self.temperature_K = self.compute_temperature()  # K
        self.temperature_C = self.temperature_K - 273.15  # C
        self.pressure = self.compute_pressure()  # Pa
        self.density = self.compute_density()  # kg/m3
        self.sound_speed = self.compute_sound_speed()
        self.gravity = self.compute_gravity()

    def compute_temperature(self):
        """
        Compute temperature at the given altitude.

        Returns:
            float: Temperature in Kelvin.
        """
        if self.altitude < Constants.altitude_junction:
            temperature = Constants.temperature_zero + Constants.temperature_variation_altitudem * self.altitude
        else:
            temperature = Constants.temperature_junction
        return temperature

    def compute_pressure(self):
        """
        Compute pressure at the given altitude.

        Returns:
            float: Pressure in Pascal.
        """
        if self.altitude < Constants.altitude_junction:
            pressure = Constants.pressure_zero * math.pow((self.temperature_K / Constants.temperature_zero),
                                                        (-Constants.gravity_zero / (
                                                                Constants.temperature_variation_altitudem *
                                                                Constants.R_air) ))
        else:
            pressure_junction = Constants.pressure_zero * math.pow((
                    Constants.temperature_junction / Constants.temperature_zero),(-Constants.gravity_zero / (
                    Constants.temperature_variation_altitudem * Constants.R_air)))
            pressure = pressure_junction * math.exp(-Constants.gravity_zero / (Constants.R_air * self.temperature_K) * (
                    self.altitude - Constants.altitude_junction))
        return pressure

    def compute_density(self):
        """
        Compute density at the given altitude.

        Returns:
            float: Density in kg/m^3.
        """
        if self.altitude < Constants.altitude_junction:
            density = Constants.density_zero * math.pow((self.temperature_K / Constants.temperature_zero),(-Constants.gravity_zero / (Constants.temperature_variation_altitudem * Constants.R_air) - 1))
        else:
            density_junction = Constants.density_zero *  math.pow((
                    Constants.temperature_junction / Constants.temperature_zero),(-Constants.gravity_zero / (
                    Constants.temperature_variation_altitudem * Constants.R_air) - 1))
            density = density_junction * math.exp(-Constants.gravity_zero / (Constants.R_air * self.temperature_K) * (
                    self.altitude - Constants.altitude_junction))
        return density



    def compute_sound_speed(self):
        """
        Compute the speed of sound at a given temperature using the ideal gas law.

        Args:
            temperature (float): Temperature in Kelvin.

        Returns:
            float: Speed of sound in meters per second.
        """

        speed_of_sound = math.sqrt(Constants.gamma_air * Constants.R_air * self.temperature_K) # m/s

        return speed_of_sound

    def compute_gravity(self):
        """
        Compute gravity at the given altitude.

        Returns:
            float: Gravity in m/s^2.
        """
        G = Constants.gravity_zero  # gravitational acceleration in m/s^2
        rayon_terre = Constants.earth_radius  # Earth radius in meters
        return G * (rayon_terre / (rayon_terre + self.altitude)) ** 2
