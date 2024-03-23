import PyPlanePackage as ppp
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Usage of the iterate_take_off_weight function
# ---------------------------------------------------------------------
M_cruise = 0.82  # Cruising speed
H_cruise = 40000  # Altitude in ft
A = 10.0  # Aspect ratio
TSFC = 0.45  # Specific fuel consumption lb / pound of thrust per hour
T_loiter = 45  # Loiter time in minutes
Fuel_res = 0.05  # Fraction of fuel before landing
Fuel_trap = 0.01  # Fraction of fuel in the conduits
Wpayload = 30750  # Payload weight in lbf
flight_range = 3500  # Distance in nautical miles
Type = 'transport-jet'  # Aircraft type, as in structure_factor

aircraft_weights = ppp.Weight(Type, M_cruise, H_cruise, A, TSFC, T_loiter, Fuel_res, Fuel_trap, Wpayload, flight_range)
print(aircraft_weights.take_off,aircraft_weights.fuel)