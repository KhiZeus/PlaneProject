import numpy as np
import pandas as pd
from scipy.interpolate import griddata, splev, splrep
import matplotlib.pyplot as plt

def wave_drag(M, H, S, Dmax, L_tot, Lsection_const, epais_rel, sweep, lift_coefficient, scri):
    """
    Evaluation of the aircraft wave drag using an approximate method presented by Raymer
    in Aircraft Design: A Conceptual Approach, 1999.

    Args:
        M (float): Cruise speed of the aircraft.
        H (float): Cruise altitude in feet.
        S (float): Wing surface area in ft^2.
        Dmax (float): Maximum diameter of the fuselage in ft.
        L_tot (float): Total length of the fuselage in ft.
        Lsection_const (float): Length of the fuselage with constant section (Dmax) in ft.
        epais_rel (float): Maximum thickness of the airfoil divided by the chord.
        sweep (float): Wing sweep at quarter chord in degrees.
        lift_coefficient (float): Cruise flight lift coefficient.
        scri (str): 'oui' if the airfoil is a supercritical airfoil.

    Returns:
        float: Wave drag in lbf.
    """
    # Mach number at zero-lift divergence
    mdd_cl0_data = pd.read_csv('wave_drag_interpolation_data/fig12_28.txt', delim_whitespace=True, header=None)
    mdd_cl0_filtered = mdd_cl0_data[['sweep', 'rel_thickness', 'mdd']].values
    if scri == 'oui':
        # Supercritical airfoil thickness correction factor
        epais_rel_eff = 0.6 * epais_rel
    else:
        epais_rel_eff = epais_rel

    epais_rel_eff = max(0.04, min(0.12, epais_rel_eff))
    mdd_eff_cl0 = griddata((mdd_cl0_filtered[:, 0], mdd_cl0_filtered[:, 1]), mdd_cl0_filtered[:, 2],
                           (epais_rel_eff, sweep))

    # LF factor evaluation
    lfdd_data = pd.read_csv('wave_drag_interpolation_data/fig12_29.txt', delim_whitespace=True, header=None)
    lfdd_filtered = lfdd_data[(lfdd_data[1] == lift_coefficient) & (lfdd_data[0] == epais_rel_eff)].values
    lfdd_eff = griddata((lfdd_filtered[:, 0], lfdd_filtered[:, 1]), lfdd_filtered[:, 2],
                        (epais_rel_eff, lift_coefficient))

    # Mach number at non-zero lift divergence
    mdd = mdd_eff_cl0 * lfdd_eff - 0.05 * lift_coefficient

    # Estimation of Sears-Haack body wave drag coefficient
    Amax = np.pi * (Dmax / 2) ** 2 / 4
    l = L_tot - Lsection_const
    cd_w_sh = 9 * np.pi / (2 * S) * (Amax / l) ** 2

    # Wave drag coefficients at different Mach numbers
    mach = np.array([1.2, 1.05, 1.0, mdd, mdd - 0.08])
    cd_w = np.array([4 * cd_w_sh, 4 * cd_w_sh, 2 * cd_w_sh, 0.002, 0.0])

    # Interpolation of wave drag value
    spl = splrep(mach, cd_w)
    cd_w_cruise = splev(M, spl)

    # Speed in ft/s
    vc = M * 1116.4370079

    # Air density at cruise altitude in slugs/ft^3
    dc = 0.0023769 * np.exp(-H / 20806)

    # Wave drag in cruise
    d = cd_w_cruise * (0.5 * dc * vc ** 2 * S)

    return d

# Example usage:
cruise_speed = 0.78
altitude = 35000
wing_surface = 860
Dmax = 12.0
total_length = 100.0
length_constant_section = 65.0
rel_thickness = 0.12
sweep = 25
lift_coefficient = 0.45
scrit = 'oui'

wave_drag_lbf = wave_drag(cruise_speed, altitude, wing_surface, Dmax, total_length, length_constant_section,
                              rel_thickness, sweep, lift_coefficient, scrit)
print("Wave drag: {} lbf".format(wave_drag_lbf))
