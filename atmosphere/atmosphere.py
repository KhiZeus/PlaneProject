import math

class Atmosphere:
    def __init__(self, altitude = 1000):
        self.altitude = altitude # meters
        self.temperature_K = self.compute_temperature() # K
        self.temperature_C = self.temperature_K - 273.15 # C
        self.pressure = self.compute_pressure() # Pa
        self.density = self.compute_density() # kg/m3
        self.gravity = self.compute_gravity()

    def compute_pressure(self):
        p0 = 101325  # Pa - Pression standard au niveau de la mer
        pressure = p0 * (1 - 0.0000225577 * self.altitude) ** 5.25588  # Pa - https://fr.wikipedia.org/wiki/Formule_du_nivellement_barom%C3%A9trique
        return pressure

    def compute_density(self):
        g = 9.81  # m/s^2
        M = 0.0289644  # kg/mol - Masse molaire de l'air
        R = 8.31447  # J/(mol*K) - Constante des gaz parfaits
        T0 = 288.15  # K - Température standard au niveau de la mer

        density = self.pressure * M / (R * self.temperature_K)  # kg/m^3 - Densité de l'air en fonction de la pression et de la température, equation gaz parfait
        return density

    def compute_temperature(self):
        # Supposons que la température de l'air diminue avec l'altitude selon la formule suivante :
        # T = T0 - L * h, où T0 est la température à une altitude de 0 mètres,
        # L est la constante de gradient thermique, et h est l'altitude en mètres
        T0 = 288.15  # K
        L = 0.0065  # K/m
        return T0 - L * self.altitude

    def compute_gravity(self):
        G = 9.81  # accélération gravitationnelle en m/s^2
        rayon_terre = 6.371e6  # rayon de la Terre en mètres
        return G * (rayon_terre / (rayon_terre + self.altitude))**2