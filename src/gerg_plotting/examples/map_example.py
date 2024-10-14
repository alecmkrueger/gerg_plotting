from gerg_plotting import Data,MapPlot,Bounds,ScatterPlot
from gerg_plotting.utils import generate_random_point
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


bounds = Bounds(lat_min = 23,lat_max = 30.5,lon_min = -98,lon_max = -88)

n_points = 100

lats,lons = np.transpose([generate_random_point(lat_min=bounds.lat_min,
                                                lat_max=bounds.lat_max,
                                                lon_min=bounds.lon_min,
                                                lon_max=bounds.lon_max) for _ in range(n_points)])
salt = np.random.uniform(low=28,high=32,size=n_points)
temp = np.random.uniform(low=5,high=28,size=n_points)
depth = np.random.uniform(low=-200,high=0,size=n_points)
time = pd.Series(pd.date_range(start='10-01-2024',end='10-10-2024',periods=n_points)).apply(mdates.date2num)

data = Data(lat=lats,lon=lons,salinity=salt,temperature=temp,depth=depth,time=time)

plotter = MapPlot(instrument=data)

plotter.scatter(var='temperature')

