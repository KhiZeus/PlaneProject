import numpy as np
from PyPlanePackage.atmosphere import Atmosphere
from scipy.optimize import fsolve


def wing_loading_landing(altitude_landing, lift_coefficient, landing_distance):
    """
    Evaluate the wing loading required for landing.

    Parameters:
    altitude_landing: Altitude at landing (ft)
    lift_coefficient: Lift coefficient of the wing during landing
    landing_distance: Landing distance (ft)

    Returns:
    wing_loading: Wing loading for landing (lbf/ft^2)
    """

    # Density ratio at landing
    sigma = Atmosphere(altitude_landing).density / Atmosphere(0).density

    # Lift pressure in lbf/ft^2
    lift_pressure = fsolve(lambda x: landing_distance - 118 * x - 400, [0, 1e6])[0]

    # Wing loading in lbf/ft^2
    wing_loading = fsolve(lambda x: lift_pressure - x * 1 / (lift_coefficient * sigma), [0, 1e3])[0]

    return wing_loading


def wing_loading_cruise(zero_lift_drag_coefficient, aspect_ratio, cruise_altitude, speed, engine_type):
    """
    Evaluate the optimal wing loading at altitude H.

    Parameters:
    zero_lift_drag_coefficient: Zero-lift drag coefficient of the aircraft
    aspect_ratio: Aspect ratio
    cruise_altitude: Cruise altitude (ft)
    speed: Cruise speed (ft/s)
    engine_type: Type of engine, either 'prop' for propeller-driven or 'jet' for jet-powered

    Returns:
    wing_loading: Wing loading (lbf/ft^2)
    """

    # Density at altitude H
    density = Atmosphere(cruise_altitude).density

    # Oswald's efficiency factor
    e = oswald_efficiency(aspect_ratio)

    # Coefficient k
    k = 1 / (np.pi * aspect_ratio * e)

    # Optimal wing loading depends on the type of engine:
    # propeller-driven aircraft must fly at maximum L/D to maximize distance,
    # while jet-powered aircraft must maximize L^0.5/D to maximize distance
    if engine_type.lower() == 'prop':
        wing_loading = density * speed ** 2 * 0.5 * np.sqrt(zero_lift_drag_coefficient / k)
    elif engine_type.lower() == 'jet':
        wing_loading = density * speed ** 2 * 0.5 * np.sqrt(zero_lift_drag_coefficient / (3 * k))
    else:
        raise ValueError("Invalid engine type. Must be 'prop' or 'jet'.")

    return wing_loading


def wing_loading_climb(thrust_weight_ratio, zero_lift_drag_coefficient, aspect_ratio, altitude, rate_of_climb, speed):
    """
    Calculate the wing loading for a given climb angle.

    Parameters:
    thrust_weight_ratio: Thrust-to-weight ratio
    zero_lift_drag_coefficient: Zero-lift drag coefficient of the aircraft
    aspect_ratio: Aspect ratio
    altitude: Altitude at the beginning of climb (ft)
    rate_of_climb: Rate of climb (ft/min)
    speed: Climb speed (ft/s)

    Returns:
    sufficient_trust: Boolean indicating if there is sufficient thrust
    wing_loading: Wing loading (lbf/ft^2)
    twmin: Minimum thrust-to-weight ratio required for climb
    """

    # Conversion of speed to ft/s
    velocity = speed

    # Evaluation of the climb angle
    alpha = np.arcsin(rate_of_climb / (60 * velocity))

    # Density at the beginning of climb
    density = Atmosphere(altitude).density

    # Oswald's efficiency factor
    e = oswald_efficiency(aspect_ratio)

    # Coefficient k
    k = 1 / (np.pi * aspect_ratio * e)

    # Evaluation of the minimum thrust-to-weight ratio for the climb angle
    twmin = np.sin(alpha) + 2 * np.cos(alpha) * np.sqrt(zero_lift_drag_coefficient * k)

    sufficient_trust = not (thrust_weight_ratio < twmin)
    if thrust_weight_ratio < twmin:
        # Insufficient thrust
        wing_loading = 0
        print('Insufficient thrust')
    else:
        a = thrust_weight_ratio - np.sin(alpha)
        denom = 2 * np.cos(alpha) ** 2 * k / (0.5 * density * velocity ** 2)
        # Calculation of the largest positive wing loading (less restrictive)
        wing_loading = (a + np.sqrt(a ** 2 - 4 * zero_lift_drag_coefficient * np.cos(alpha) ** 2 * k)) / denom

    return sufficient_trust, wing_loading, twmin


def wing_loading_takeoff(altitude_takeoff, lift_coefficient, thrust_weight_ratio, takeoff_distance):
    """
    Evaluate the wing loading required for takeoff.

    Parameters:
    altitude_takeoff: Takeoff altitude (ft)
    lift_coefficient: Lift coefficient of the wing during takeoff
    thrust_weight_ratio: Thrust-to-weight ratio at takeoff
    takeoff_distance: Takeoff distance (ft)

    Returns:
    wing_loading: Wing loading for takeoff (lbf/ft^2)
    """

    # Density ratio at takeoff
    sigma = Atmosphere(altitude_takeoff).density / Atmosphere(0).density

    # Takeoff pressure in lbf/ft^2
    takeoff_pressure = fsolve(lambda x: takeoff_distance - 20.9 * x - 87 *
                                        (x * thrust_weight_ratio) ** 0.5, [0, 1e6])[0]

    # Wing loading in lbf/ft^2
    wing_loading = fsolve(lambda x: takeoff_pressure - x * 1 / (lift_coefficient *
                                                                thrust_weight_ratio * sigma), [0, 1e3])[0]

    return wing_loading


def oswald_efficiency(aspect_ratio):
    """
    Returns the Oswald efficiency factor as a constant value.

    Parameters:
    aspect_ratio: Aspect ratio of the aircraft

    Returns:
    oswald_efficiency_factor: Oswald efficiency factor
    """
    return 0.8
