import math
from PyPlanePackage.atmosphere import Atmosphere
from scipy.optimize import fsolve
import numpy as np

class Weight:
    """
    Represents the weight characteristics of an aircraft.
    """

    def __init__(self, Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, flight_range):
        """
        Initialize the Weight class.

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
            flight_range (float): Distance in nautical miles.
        """
        self.take_off, self.empty, self.fuel = self.iterate_take_off_weight(Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, flight_range)
        self.payload = Wpayload
        self.structure_factor = self.structure_factor(Type, self.take_off)
    def iterate_take_off_weight(self, Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, flight_range):
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
            flight_range (float): Distance in nautical miles.

        Returns:
            Tuple[float, float, float]: Take-off weight, empty weight, fuel weight.
        """

        # Find the value of Wto in an interval
        Wto = fsolve(lambda Wto: self.fpoids(Wto, flight_range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap, M_cruise, H_cruise),
                     Wpayload, xtol=1e-6)[0]

        # Calculate the structure factor corresponding to Wto
        Sfactor = self.structure_factor(Type, Wto)

        # Calculate Wfuel, Wempty
        Wempty = Sfactor * Wto
        Wfuel = Wto - Wempty - Wpayload
        return Wto, Wempty, Wfuel

    def fpoids(self, Wto, Range, Type, Wpayload, TSFC, T_loiter, A, Fuel_res, Fuel_trap,M_cruise,H_cruise):
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

        resw = 1 - (Wpayload / Wto + self.structure_factor(Type, Wto) +
                    (1 - fdec * self.fclimb(M_cruise)) * (1 + self.fcruise(M_cruise,H_cruise, A, Range, TSFC) *
                                                          self.floiter(M_cruise, T_loiter, TSFC, A)))
        return resw

    def fclimb(self, M_cruise):
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

    def floiter(self, M_cruise, T_loiter, TSFC, A):
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
        ldmax = self.finesse(M_cruise, A)
        flinv = np.exp(T_loiter * TSFC / (ldmax * 60))
        fl = 1 / flinv
        return fl

    def fcruise(self, M_cruise, H_cruise,  A, Range, TSFC):
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
        ldmax = self.finesse(M_cruise, A)
        ld = 0.866 * ldmax
        vc = self.vitesse(M_cruise, H_cruise)
        fcinv = np.exp(Range * TSFC * 6080 / (vc * ld * 3600))
        fc = 1 / fcinv
        return fc

    def structure_factor(self, Type, Wto):
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

    def finesse(self, Mach, A):
        """
        Estimate the maximum finesse.

        Args:
            Mach (float): Mach number.
            A (float): Aspect ratio.

        Returns:
            float: Maximum finesse (ratio L/D max).
        """
        if Mach < 1:
            x = A + 10
        else:
            x = 11 * Mach ** -0.5
        return x

    def vitesse(self,mach, altitude):
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

