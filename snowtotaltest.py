import numpy as np
#from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import math
from metpy.interpolate import natural_neighbor_to_grid

# Load data from CSV file
data = np.genfromtxt('Jan1617.csv', delimiter=',')
lat = data[:,2]
lon = data[:,1]
elevation = data[:,3]
snowfall = data[:,4]

# Set up a uniform grid with 0.1 degree resolution
lats = np.arange(lat.min(), lat.max(), 0.01)
lons = np.arange(lon.min(), lon.max(), 0.01)
xi, yi = np.meshgrid(lons, lats)

# Interpolate the data using natural neighbor interpolation
#zi = griddata((lon, lat), snowfall, (xi, yi), method='cubic', fill_value=0)
zi = natural_neighbor_to_grid(lon, lat, snowfall, xi, yi)
zi = np.clip(zi, snowfall.min(), snowfall.max())

from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Set up the plot
#fig, ax = plt.subplots()

# Plot the interpolated data using a color map
#c = ax.pcolormesh(lats, lons, zi, cmap='Blues')
proj = ccrs.Mercator()
ax = plt.axes(projection=proj)

c = plt.contourf(lons, lats, zi, levels=9,transform=ccrs.PlateCarree(), cmap='Blues', vmin=0, vmax=10)

cb=plt.colorbar(c, ax=ax)
#cb.set_limits(0, 10)
cb.set_ticks([0,1,2,4,6,8])
cb.set_ticklabels(['0','1','2','4','6','8'])

# Add a color bar
#cb = fig.colorbar(c, ax=ax)
cb.set_label('Snowfall (In)')

# Add axis labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle="--")
ax.add_feature(cfeature.STATES)

# Show the plot
plt.show()
