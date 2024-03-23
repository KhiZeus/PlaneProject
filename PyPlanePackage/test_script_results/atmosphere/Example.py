"""This is a sample  of Plane project use """
import PyPlanePackage as ppp
import  numpy as np
import matplotlib.pyplot as plt
# Create an instance of the Atmosphere class


# Generate altitude data
altitudes = np.linspace(0, 35000, 100)

# Calculate temperature and pressure values for the given altitudes
temperatures = [ppp.Atmosphere(alt).temperature_K for alt in altitudes]
pressures = [ppp.Atmosphere(alt).pressure for alt in altitudes]
densities = [ppp.Atmosphere(alt).density for alt in altitudes]
viscosities = [ppp.Atmosphere(alt).viscosity for alt in altitudes]
sound_speeds = [ppp.Atmosphere(alt).sound_speed for alt in altitudes]

# Plotting
fig, axs = plt.subplots(5, 1, figsize=(8, 24))

# Plot temperature vs altitude
axs[0].plot(altitudes, temperatures, label='Temperature', color='blue')
axs[0].set_ylabel('Temperature (°C)', color='blue')
axs[0].tick_params(axis='y', labelcolor='blue')
axs[0].grid(True)
axs[0].legend()

# Plot pressure vs altitude with scientific notation
axs[1].plot(altitudes, pressures, label='Pressure', color='red')
axs[1].set_ylabel('Pressure (hPa)', color='red')
axs[1].tick_params(axis='y', labelcolor='red')
# Set scientific notation for pressure
axs[1].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
axs[1].grid(True)
axs[1].legend()

# Plot density vs altitude
axs[2].plot(altitudes, densities, label='Density', color='green')
axs[2].set_ylabel('Density (kg/m³)', color='green')
axs[2].tick_params(axis='y', labelcolor='green')
# Set scientific notation for pressure
axs[2].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
axs[2].grid(True)
axs[2].legend()

# Plot viscosity vs altitude
axs[3].plot(altitudes, viscosities, label='Viscosity', color='orange')
axs[3].set_ylabel('Viscosity (kg/(m*s))', color='orange')
axs[3].tick_params(axis='y', labelcolor='orange')
axs[3].grid(True)
axs[3].legend()

# Plot sound speed vs altitude
axs[4].plot(altitudes, sound_speeds, label='Sound Speed', color='purple')
axs[4].set_ylabel('Sound Speed (m/s)', color='purple')
axs[4].set_xlabel('Altitude (km)')
axs[4].tick_params(axis='y', labelcolor='purple')
axs[4].grid(True)
axs[4].legend()

# Add title
plt.suptitle('Atmospheric Properties vs Altitude', fontsize=16)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the plots in a PDF file with each plot on a different page
plt.savefig('atmospheric_properties.pdf')

# Show plot
plt.show()