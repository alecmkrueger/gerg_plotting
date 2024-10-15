from gerg_plotting import Data,MapPlot,Bounds,Variable
from gerg_plotting.utils import generate_random_point
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean

# Generate Test Data
bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
data_bounds = Bounds(lat_min = 27,lat_max = 28.5,lon_min = -96,lon_max = -89,depth_top=-1,depth_bottom=1000)
n_points = 1000
lats,lons = np.transpose([generate_random_point(lat_min=data_bounds.lat_min,
                                                lat_max=data_bounds.lat_max,
                                                lon_min=data_bounds.lon_min,
                                                lon_max=data_bounds.lon_max) for _ in range(n_points)])
salinity = np.random.uniform(low=28,high=32,size=n_points)
temperature = np.random.uniform(low=5,high=28,size=n_points)
depth = np.random.uniform(low=0,high=200,size=n_points)
time = pd.Series(pd.date_range(start='10-01-2024',end='10-10-2024',periods=n_points)).apply(mdates.date2num)

# Init Data object
data = Data(lat=lats,lon=lons,salinity=salinity,temperature=temperature,depth=depth,time=time)
data.add_custom_variable(Variable(data = np.random.uniform(7.7,8.1,n_points), name = 'pH', cmap=cmocean.cm.thermal, units=None, vmin=7.7, vmax=8.1, label='pH'))

# Init subplots (optional)
fig,ax = plt.subplots(figsize=(10,15),nrows=4,subplot_kw={'projection': ccrs.PlateCarree()},layout='constrained')
# Init MapPlot object
plotter = MapPlot(instrument=data,bounds=bounds,grid_spacing=3)
# Generate Scatter plots on one figure
plotter.scatter(fig=fig,ax=ax[0],var='temperature',show_bathy=True,pointsize=30)
plotter.scatter(fig=fig,ax=ax[1],var='salinity',show_bathy=True,pointsize=30)
plotter.scatter(fig=fig,ax=ax[2],var='depth',show_bathy=True,pointsize=30)
plotter.scatter(fig=fig,ax=ax[3],var='time',show_bathy=True,pointsize=30)
# fig.savefig('map_example.png',dpi=500,bbox_inches='tight')