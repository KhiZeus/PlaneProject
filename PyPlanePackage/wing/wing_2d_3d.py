import numpy as np
from PyPlanePackage.atmosphere import Atmosphere


def wing_drag(speed, altitude, leading_edge_sweep, wing_area, aspect_ratio, relative_thickness,
              x_max_thickness, taper_ratio, interference_factor, cruise_weight):
    """
    Evaluate the drag of an aircraft wing using relations partly derived from Corke, Design of Aircraft, chapter 4, 2003
    Parameters:
    speed: Cruise speed of the aircraft
    altitude: Cruise altitude (ft)
    leading_edge_sweep: Leading edge sweep angle (degree)
    wing_area: Wing surface area (ft^2)
    aspect_ratio: Aspect ratio of the wing
    relative_thickness: Maximum thickness of the airfoil divided by the chord
    x_max_thickness: Ratio x/c of the position of the maximum relative thickness
    taper_ratio: Taper ratio of the wing
    interference_factor: Wing interference factor
    cruise_weight: Aircraft weight during cruise (lbf)

    Returns:
    total_drag: Total wing drag (lbf)
    zero_lift_drag: Zero-lift drag of the wing (lbf)
    """

    # Density at cruise altitude
    density_cruise = Atmosphere(altitude).density

    # Viscosity at cruise altitude
    viscosity_cruise = Atmosphere(altitude).viscosity

    # Wing span, root chord, and mean aerodynamic chord
    span = np.sqrt(wing_area * aspect_ratio)
    root_chord = 2 * span / (aspect_ratio * (1 + taper_ratio))
    mean_chord = (2 * root_chord * (1 + taper_ratio + taper_ratio ** 2)) / (3 * (1 + taper_ratio))

    # Mid-chord sweep angle
    mid_chord_sweep = np.arctan(
        np.tan(np.radians(leading_edge_sweep)) - 0.5 * (2 * root_chord / span) * (1 - taper_ratio))

    # Sweep angle at maximum thickness
    max_thickness_sweep = np.arctan(
        np.tan(np.radians(leading_edge_sweep)) - x_max_thickness * (2 * root_chord / span) * (1 - taper_ratio))

    # Reynolds number
    reynolds_number = density_cruise * speed * mean_chord / viscosity_cruise

    # Effective Mach number
    effective_mach = speed * np.cos(np.radians(mid_chord_sweep)) / Atmosphere(altitude).sound_speed

    # Evaluation of the friction coefficient for a flat plate
    if reynolds_number <= 5e5:
        cf = 1.328 / np.sqrt(reynolds_number)
    else:
        cf = 0.455 / ((np.log10(reynolds_number)) ** 2.58 * (1 + 0.144 * effective_mach ** 2) ** 0.65)

    # Evaluation of the form factor
    form_factor = (1 + 0.6 / x_max_thickness * relative_thickness + 100 * relative_thickness ** 4) * \
                  (1.34 * speed ** 0.18 * (np.cos(np.radians(max_thickness_sweep))) ** 0.28)

    # Wetted area of the wing
    if relative_thickness <= 0.05:
        wetted_area = 2.003 * wing_area
    else:
        wetted_area = wing_area * (1.977 + 0.52 * relative_thickness)

    # Wing zero-lift drag coefficient
    cd0 = cf * form_factor * interference_factor * wetted_area / wing_area

    # Oswald's efficiency factor
    oswald_efficiency_factor = e_oswald_wing(aspect_ratio)

    # Lift coefficient
    lift_coefficient = cruise_weight / (0.5 * density_cruise * speed ** 2 * wing_area)

    # Total wing drag coefficient with induced drag
    total_drag_coefficient = cd0 + (1 / (np.pi * aspect_ratio * oswald_efficiency_factor)) * lift_coefficient ** 2

    # Zero-lift drag and total wing drag
    zero_lift_drag = cd0 * (0.5 * density_cruise * speed ** 2 * wing_area)
    total_drag = total_drag_coefficient * (0.5 * density_cruise * speed ** 2 * wing_area)

    return total_drag, zero_lift_drag


def lift_slope_3d(speed, altitude, wing_area, aspect_ratio, taper_ratio, leading_edge_sweep, profile_slope):
    """
    Evaluate the variation of lift with angle of attack in 3D using relations from Anderson,
    Aircraft performance and design, 1999.

    Parameters:
    speed: Aircraft speed (ft/s)
    altitude: Altitude (ft)
    wing_area: Wing surface area (ft^2)
    aspect_ratio: Aspect ratio of the wing
    taper_ratio: Taper ratio of the wing
    leading_edge_sweep: Leading edge sweep angle of the wing (degree)
    profile_slope: Slope of the profile in 1/degree

    Returns:
    lift_slope: Lift slope of the wing (1/degree)
    """

    # Wing span and root chord
    span = np.sqrt(wing_area * aspect_ratio)
    root_chord = 2 * span / (aspect_ratio * (1 + taper_ratio))

    # Mach number
    mach = speed / Atmosphere(altitude).sound_speed

    # Mid-chord sweep angle
    mid_chord_sweep = np.arctan(
        np.tan(np.radians(leading_edge_sweep)) - 0.5 * (2 * root_chord / span) * (1 - taper_ratio))

    # Equivalent slope of the profile for a swept wing
    profile_slope_eq = profile_slope * 180 / np.pi * np.cos(np.radians(mid_chord_sweep))

    # Calculation of the lift slope in 3D using Anderson's equation for a wing with equivalent sweep to that of Raymer
    lift_slope_eq = profile_slope_eq / (np.sqrt(
        1 - (mach * np.cos(np.radians(mid_chord_sweep))) ** 2 + (profile_slope_eq / (np.pi * aspect_ratio)) ** 2) +
                                        profile_slope_eq / (np.pi * aspect_ratio))

    # Conversion to radians
    lift_slope = lift_slope_eq * np.pi / 180

    return lift_slope


def e_oswald_wing(aspect_ratio):
    """
    Returns the Oswald efficiency for wing only factor as a constant value.

    Parameters:
    aspect_ratio: Aspect ratio of the aircraft

    Returns:
    e: Oswald efficiency factor
    """
    return 0.95
