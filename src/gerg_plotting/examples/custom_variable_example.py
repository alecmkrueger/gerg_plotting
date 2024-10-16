from gerg_plotting import Data,MapPlot,Bounds,ScatterPlot,Histogram,Variable
from gerg_plotting.utils import generate_random_point
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import cmocean

# Generate Test Data
bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
data_bounds = Bounds(lat_min = 27,lat_max = 28.5,lon_min = -96,lon_max = -89,depth_top=-1,depth_bottom=1000)
n_points = 1000
lats,lons = np.transpose([generate_random_point(lat_min=data_bounds.lat_min,
                                                lat_max=data_bounds.lat_max,
                                                lon_min=data_bounds.lon_min,
                                                lon_max=data_bounds.lon_max) for _ in range(n_points)])
depth = np.random.uniform(low=-200,high=0,size=n_points)
time = pd.Series(pd.date_range(start='10-01-2024',end='10-10-2024',periods=n_points)).apply(mdates.date2num)
salinity = np.random.uniform(low=28,high=32,size=n_points)
temperature = np.random.uniform(low=5,high=28,size=n_points)

# Init Data object
data = Data(lat=lats,lon=lons,depth=depth,time=time,salinity=salinity,temperature=temperature)
# Init pH Variable object
pH = Variable(data=np.random.normal(7.7,scale=0.15,size=n_points),name='pH',cmap=cmocean.cm.thermal)
# Add the pH Variable object to the Data object
data.add_custom_variable(pH)
# Test by plotting a histogram
Histogram(data).plot(var='pH')

MapPlot(data,bounds=bounds).scatter('pH',pointsize=30)

ScatterPlot(data).depth_time_series(var='pH')
