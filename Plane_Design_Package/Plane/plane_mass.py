import numpy as np
from scipy.optimize import fsolve


def itertow(Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, Range):
    # ---------------------------------------------------------------------
    # Values input to the function
    # ---------------------------------------------------------------------
    # Type: aircraft type according to Corke
    # M_cruise: cruising Mach number
    # H_cruise: cruising altitude in ft
    # A: aspect ratio
    # TSFC: specific fuel consumption lb / pound of thrust per hour
    # T_loiter: loiter time in minutes
    # Fuel_res: fraction of fuel before landing
    # Fuel_trap: fraction of fuel in the conduits
    # Wpayload: payload weight in lbf
    # Range: distance in nautical miles

    # ---------------------------------------------------------------------
    # Values returned by the function
    # ---------------------------------------------------------------------
    # Wto: total takeoff weight, lbf
    # Wfuel: fuel weight at takeoff, lbf
    # Wempty: empty weight, without payload, lbf

    # ---------------------------------------------------------------------
    # Find the value of Wto in an interval
    # We seek the zeros of the residue function
    # ---------------------------------------------------------------------
    Wto = fsolve(lambda Wto: fpoids(Wto, Range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap),
                 Wpayload, xtol=1e-6)[0]

    # ---------------------------------------------------------------------
    # Calculate the structure factor corresponding to Wto
    # ---------------------------------------------------------------------
    Sfactor = structure_factor(Type, Wto)

    # ---------------------------------------------------------------------
    # Calculate Wfuel, Wempty
    # ---------------------------------------------------------------------
    Wempty = Sfactor * Wto
    Wfuel = Wto - Wempty - Wpayload

    # ---------------------------------------------------------------------
    # Screen output
    # ---------------------------------------------------------------------
    print('Wto=', Wto)
    print('Wempty=', Wempty)
    print('Wfuel=', Wfuel)
    print('Structure factor', Sfactor)


def fpoids(Wto, Range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap):
    # ---------------------------------------------------------------------
    # Function to calculate takeoff weight
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Fraction of weight at takeoff
    # ---------------------------------------------------------------------
    fdec = 0.975
    # ---------------------------------------------------------------------
    # Fraction of weight at landing
    # ---------------------------------------------------------------------
    fland = 0.975

    # ---------------------------------------------------------------------
    # Residue function
    # ---------------------------------------------------------------------
    resw = 1 - (Wpayload / Wto + structure_factor(Type, Wto) +
                (1 - fdec * fclimb(M_cruise)) * (1 + fcruise(M_cruise, H_cruise, A, Range, TSFC) *
                                                 floiter(M_cruise, H_cruise, T_loiter, TSFC, A)))
    return resw


def fclimb(M_cruise):
    # ---------------------------------------------------------------------
    # Function to calculate climb weight fraction
    # ---------------------------------------------------------------------
    if M_cruise < 1:
        fc = 1 - 0.04 * M_cruise
    else:
        fc = 0.96 - 0.03 * (M_cruise - 1)
    return fc


def floiter(M_cruise, H_cruise, T_loiter, TSFC, A):
    # ---------------------------------------------------------------------
    # Function to calculate loiter weight fraction
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # Estimate of the maximum finesse
    # ---------------------------------------------------------------------
    ldmax = finesse(M_cruise, A)
    # ---------------------------------------------------------------------
    # Loiter time is in minutes
    # ---------------------------------------------------------------------
    flinv = np.exp(T_loiter * TSFC / (ldmax * 60))
    fl = 1 / flinv
    return fl


def fcruise(M_cruise, H_cruise, A, Range, TSFC):
    # ---------------------------------------------------------------------
    # Function to calculate cruise weight fraction
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # Estimate of the maximum finesse
    # ---------------------------------------------------------------------
    ldmax = finesse(M_cruise, A)
    # ---------------------------------------------------------------------
    # For a jet aircraft, maximum range at 0.866*ldmax
    # ---------------------------------------------------------------------
    ld = 0.866 * ldmax
    # ---------------------------------------------------------------------
    # Cruise speed ft/s
    # ---------------------------------------------------------------------
    vc = vitesse(M_cruise, sound_speed)*3.2808
    # ---------------------------------------------------------------------
    # Range is in nautical miles
    # ---------------------------------------------------------------------
    fcinv = np.exp(Range * TSFC * 6080 / (vc * ld * 3600))
    fc = 1 / fcinv
    return fc


def structure_factor(Type, Wto):
    # Evaluation of the initial structure factor of an aircraft using a
    # relation from Corke, Design of aircraft, chapter 1, 2003

    # Values input to the function
    # Type: aircraft type according to Corke
    # Wto: total takeoff weight, lbf

    # Value returned by the function
    # sf: structure factor

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
    # Estimation of the maximum finesse using a relation from
    # Corke, Design of aircraft, chapter 1, 2003

    # Values input to the function
    # M: Mach number
    # A: aspect ratio

    # Value returned by the function
    # x: maximum finesse (ratio L/D max)

    if M < 1:
        x = A + 10
    else:
        x = 11 * M ** -0.5
    return x


def vitesse(Mach, sound_speed):
    # Cruise speed m/s

    # Values input to the function
    # M: Mach number
    # H: altitude in ft

    # Value returned by the function
    # Cruise speed in ft/s

    # Temperature at altitude

    # Speed of sound


    # Flight speed in ft/s
    vc = Mach * sound_speed

    return vc


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
