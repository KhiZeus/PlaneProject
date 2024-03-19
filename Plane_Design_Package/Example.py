"""This is a sample  of Plane project use """

#from Plane_Design_Package import constants
import constants
from atmosphere import Atmosphere
atm = Atmosphere(altitude=25000)
g=atm.density

print(g)