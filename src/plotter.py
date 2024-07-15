import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
from plotter_classes import SurfacePlot,Glider,DepthPlot,Bounds,Histogram
from utils.plotter_utils import interp_data,filter_var,get_bathy

ds = xr.open_dataset('../test_data/2024_mission_44.nc')

df = interp_data(ds)

df['salinity'] = filter_var(df['salinity'],30,40)


df = df.where(df.time>pd.to_datetime('2024-01-01'))
df. dropna()
df = df[::100]


temperature = df['temperature'].values
salinity = df['salinity'].values
latitude = df['latitude'].values
longitude = df['longitude'].values
depth = df['pressure'].values
dates = df['time'].values


glider = Glider(lat = latitude,
                lon = longitude,
                depth = depth,
                time = dates,
                temperature = temperature,
                salinity = salinity)

# bounds = Bounds(lat_min=18,
#                 lat_max=24,
#                 lon_max=278,
#                 lon_min=271,
#                 depth_bottom=1000,
#                 depth_top=None)

bounds = Bounds(lat_max=None)
x,y,z = get_bathy(map_bounds=bounds)

# fig,axes = plt.subplots(nrows=7,figsize = (10,35))
# surfaces = SurfacePlot(instrument=glider,bounds=bounds)
# surfaces.map(fig=fig,ax=axes[0],var='time')

# depth_plot = DepthPlot(instrument=glider,bounds=bounds)

# depth_plot.time_series(fig=fig,ax=axes[1],var='temperature')
# depth_plot.var_var(fig=fig,ax=axes[2],x='salinity',y='temperature',color_var='salinity')
# depth_plot.var_var(fig=fig,ax=axes[3],x='temperature',y='depth',color_var='salinity')
# depth_plot.ax.invert_yaxis()

# hist = Histogram(instrument=glider,bounds=bounds)
# hist.plot(fig=fig,ax=axes[4],var='temperature')
# hist.plot(fig=fig,ax=axes[5],var='salinity')
# hist.plot2d(fig=fig,ax=axes[6],x='temperature',y='depth',range=[[0, 35], [0, 1000]],bins=100,norm='log')
# hist.ax.invert_yaxis()


# plt.show()
