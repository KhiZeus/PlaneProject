"""This is a sample  of Plane project use """

import PyPlanePackage
atm = PyPlanePackage.Atmosphere(altitude=25000)
g=atm.density

print(g)