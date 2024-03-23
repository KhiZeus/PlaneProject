import numpy as np
from scipy.integrate import quad
from PyPlanePackage.atmosphere import Atmosphere


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


def trainee_fuselage(cruise_speed, altitude, wing_surface, Dmax, total_length, length_constant_section, k):
    """
    Evaluation of the wetted area and drag of the fuselage,
    Raymer's method, from Aircraft Design: A Conceptual Approach, 1999.

    Parameters:
    - cruise_speed: Cruise speed of the aircraft
    - altitude: Cruise altitude, ft
    - wing_surface: Wing surface area, ft^2
    - Dmax: Maximum diameter of the fuselage, ft
    - total_length: Total length of the fuselage, ft
    - length_constant_section: Length of the fuselage with constant section (Dmax), ft
    - k: Fuselage finishing roughness, ft

    Returns:
    - d: Fuselage friction drag
    - S_wet: Fuselage surface area, ft^2
    """

    # Density at cruise altitude
    dc = Atmosphere(altitude).density

    # Viscosity at cruise altitude
    mu = Atmosphere(altitude).viscosity

    # Geometric characteristics of the fuselage
    length_variable_section = total_length - length_constant_section

    # Define the lambda function for the perimeter
    fperim = lambda x: 2 * np.pi * Dmax / 2 * (1 - (x / (length_variable_section / 2)) ** 2) ** 0.75

    # Perform the integration using quad
    Savant, _ = quad(fperim, 0, length_variable_section / 2)

    # By symmetry, rear (tail) is identical
    Sarriere = Savant

    # Surface of the constant section: area of a cylinder with diameter Dmax
    Scentre = np.pi * Dmax * length_constant_section

    # Total fuselage surface area
    S_wet = Savant + Scentre + Sarriere

    # Evaluation of the Reynolds number for smooth surface
    Re = dc * cruise_speed * total_length / mu

    # Evaluation of the Reynolds number for rough surface
    if cruise_speed < 0.7:
        # Subsonic
        Re_cutoff = 38.21 * (total_length / k) ** 1.053
    else:
        # Transonic
        Re_cutoff = 44.62 * (total_length / k) ** 1.053 * cruise_speed ** 1.16

    rex = min(Re, Re_cutoff)

    # Evaluation of the coefficient of friction drag for a flat plate
    if rex <= 5e5:
        # Laminar
        cf = 1.328 / np.sqrt(rex)
    else:
        # Turbulent
        cf = 0.455 / ((np.log10(rex)) ** 2.58 * (1 + 0.144 * cruise_speed ** 2) ** 0.65)

    # Evaluation of the fuselage shape factor
    f = total_length / Dmax
    FF = 1 + 60 / f ** 3 + f / 400

    # Fuselage drag coefficient
    Q = 1
    cd = cf * FF * Q * S_wet / wing_surface

    # Fuselage drag in lbf
    d = cd * (0.5 * dc * cruise_speed ** 2 * wing_surface)

    return d, S_wet


def fperim(x, Dmax, length_variable_section):
    # Perimeter according to Sears-Haack shape
    r = Dmax / 2 * (1 - (x / (length_variable_section / 2)) ** 2) ** 0.75
    return 2 * np.pi * r

