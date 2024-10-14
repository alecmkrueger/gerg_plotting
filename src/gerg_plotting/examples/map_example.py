from gerg_plotting import Data,SurfacePlot,Bounds,VarPlot
from gerg_plotting.utils import generate_random_point
import numpy as np

bounds = Bounds(lat_min = 23,lat_max = 30.5,lon_min = -98,lon_max = -88)

n_points = 100

lats,lons = np.transpose([generate_random_point(lat_min=bounds.lat_min,
                                                lat_max=bounds.lat_max,
                                                lon_min=bounds.lon_min,
                                                lon_max=bounds.lon_max) for _ in range(n_points)])
salt = np.random.uniform(low=28,high=32,size=n_points)
temp = np.random.uniform(low=5,high=28,size=n_points)
depth = np.random.uniform(low=-200,high=0,size=n_points)

data = Data(lat=lats,lon=lons,salinity=salt,temperature=temp,depth=depth)

data.depth.units = ''

plotter = VarPlot(instrument=data)

plotter.TS_with_color_var('depth')

