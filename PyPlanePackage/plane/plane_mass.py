# ---------------------------------------------------------------------
#
## Estimate initial weight of an aircraft using iterative approach.
# # from Matlab version Copyright 2008: François Morency

# ---------------------------------------------------------------------
import numpy as np
from PyPlanePackage.atmosphere import Atmosphere
from scipy.optimize import fsolve

def itertow(Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, Range):
    """
    Calculate initial weight of an aircraft using iterative approach.

    Args:
        Type (str): Aircraft type according to Corke.
        M_cruise (float): Cruising Mach number.
        H_cruise (float): Cruising altitude in ft.
        A (float): Aspect ratio.
        TSFC (float): Specific fuel consumption in lb / pound of thrust per hour.
        T_loiter (float): Loiter time in minutes.
        Fuel_res (float): Fraction of fuel before landing.
        Fuel_trap (float): Fraction of fuel in the conduits.
        Wpayload (float): Payload weight in lbf.
        Range (float): Distance in nautical miles.

    Returns:
        None
    """

    # Find the value of Wto in an interval
    Wto = fsolve(lambda Wto: fpoids(Wto, Range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap),
                 Wpayload, xtol=1e-6)[0]

    # Calculate the structure factor corresponding to Wto
    Sfactor = structure_factor(Type, Wto)

    # Calculate Wfuel, Wempty
    Wempty = Sfactor * Wto
    Wfuel = Wto - Wempty - Wpayload

    #RMV Screen output
    print('Wto=', Wto)
    print('Wempty=', Wempty)
    print('Wfuel=', Wfuel)
    print('Structure factor', Sfactor)


def fpoids(Wto, Range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap):
    """
    Calculate takeoff weight.

    Args:
        Wto (float): Total takeoff weight, lbf.
        Range (float): Distance in nautical miles.
        Type (str): Aircraft type according to Corke.
        Wpayload (float): Payload weight in lbf.
        TSFC (float): Specific fuel consumption in lb / pound of thrust per hour.
        T_loiter (float): Loiter time in minutes.
        A (float): Aspect ratio.
        Fuel_res (float): Fraction of fuel before landing.
        Fuel_trap (float): Fraction of fuel in the conduits.

    Returns:
        float: Residue function.
    """
    fdec = 0.975
    fland = 0.975

    resw = 1 - (Wpayload / Wto + structure_factor(Type, Wto) +
                (1 - fdec * fclimb(M_cruise)) * (1 + fcruise(M_cruise, H_cruise, A, Range, TSFC) *
                                                 floiter(M_cruise, H_cruise, T_loiter, TSFC, A)))
    return resw


def fclimb(M_cruise):
    """
    Calculate climb weight fraction.

    Args:
        M_cruise (float): Cruising Mach number.

    Returns:
        float: Climb weight fraction.
    """
    if M_cruise < 1:
        fc = 1 - 0.04 * M_cruise
    else:
        fc = 0.96 - 0.03 * (M_cruise - 1)
    return fc


def floiter(M_cruise, H_cruise, T_loiter, TSFC, A):
    """
    Calculate loiter weight fraction.

    Args:
        M_cruise (float): Cruising Mach number.
        H_cruise (float): Cruising altitude in ft.
        T_loiter (float): Loiter time in minutes.
        TSFC (float): Specific fuel consumption in lb / pound of thrust per hour.
        A (float): Aspect ratio.

    Returns:
        float: Loiter weight fraction.
    """
    ldmax = finesse(M_cruise, A)
    flinv = np.exp(T_loiter * TSFC / (ldmax * 60))
    fl = 1 / flinv
    return fl


def fcruise(M_cruise, H_cruise, A, Range, TSFC):
    """
    Calculate cruise weight fraction.

    Args:
        M_cruise (float): Cruising Mach number.
        H_cruise (float): Cruising altitude in ft.
        A (float): Aspect ratio.
        Range (float): Distance in nautical miles.
        TSFC (float): Specific fuel consumption in lb / pound of thrust per hour.

    Returns:
        float: Cruise weight fraction.
    """
    ldmax = finesse(M_cruise, A)
    ld = 0.866 * ldmax
    vc = vitesse(M_cruise)
    fcinv = np.exp(Range * TSFC * 6080 / (vc * ld * 3600))
    fc = 1 / fcinv
    return fc


def structure_factor(Type, Wto):
    """
    Calculate the initial structure factor of an aircraft.

    Args:
        Type (str): Aircraft type according to Corke.
        Wto (float): Total takeoff weight, lbf.

    Returns:
        float: Structure factor.
    """
    type_lower = Type.lower()
    if type_lower == 'glider':
        a = 0.86
        c = -0.05
    elif type_lower == 'powered-glider':
        a = 0.91
        c = -0.05
    elif type_lower == 'indiv-constr':
        a = 1.19
        c = -0.09
    elif type_lower == 'indiv-constr(comp)':
        a = 1.15
        c = -0.09
    elif type_lower == 'gen-aviation(1eng)':
        a = 2.36
        c = -0.18
    elif type_lower == 'gen-aviation(2eng)':
        a = 1.51
        c = -0.10
    elif type_lower == 'agricultural-plane':
        a = 0.74
        c = -0.03
    elif type_lower == 'turboprop(2eng)':
        a = 0.96
        c = -0.05
    elif type_lower == 'seaplane':
        a = 1.09
        c = -0.05
    elif type_lower == 'training-jet':
        a = 1.59
        c = -0.10
    elif type_lower == 'combat-jet':
        a = 2.34
        c = -0.13
    elif type_lower == 'transport-jet':
        a = 1.02
        c = -0.06
    elif type_lower == 'bomber':
        a = 0.93
        c = -0.07
    else:
        raise ValueError('Unknown aircraft type')

    sf = a * Wto ** c
    return sf


def finesse(M, A):
    """
    Estimate the maximum finesse.

    Args:
        M (float): Mach number.
        A (float): Aspect ratio.

    Returns:
        float: Maximum finesse (ratio L/D max).
    """
    if M < 1:
        x = A + 10
    else:
        x = 11 * M ** -0.5
    return x


def vitesse(mach,altitude):
    """
    Calculate speed of sound.

    Args:
        mach (float): Mach number.
       altitude (float) : Altitude:

    Returns:
        float: Speed of sound.
    """
    atmosphere = Atmosphere(altitude)
    return mach * atmosphere.sound_speed


# ---------------------------------------------------------------------
# Usage of the itertow function
# ---------------------------------------------------------------------
M_cruise = 0.82  # Cruising speed
H_cruise = 40000  # Altitude in ft
A = 10.0  # Aspect ratio
TSFC = 0.45  # Specific fuel consumption lb / pound of thrust per hour
T_loiter = 45  # Loiter time in minutes
Fuel_res = 0.05  # Fraction of fuel before landing
Fuel_trap = 0.01  # Fraction of fuel in the conduits
Wpayload = 30750  # Payload weight in lbf
Range = 3500  # Distance in nautical miles
Type = 'jet-transport'  # Aircraft type, as in structure_factor

itertow(Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, Range)
