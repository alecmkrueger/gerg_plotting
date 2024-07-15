import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
from plotter_classes import SurfacePlot,Glider,DepthPlot,Bounds
from utils.plotter_utils import interp_data,filter_var

ds = xr.open_dataset('../test_data/2024_mission_44.nc')

df = interp_data(ds)

df['salinity'] = filter_var(df['salinity'],30,40)



# start_cutoff = 100
# end = 100000
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

bounds = Bounds(lat_min=18,
                lat_max=24,
                lon_max=278,
                lon_min=271,
                depth_bottom=1000,
                depth_top=None)

fig,axes = plt.subplots(nrows=3,figsize = (10,20))
surfaces = SurfacePlot(instrument=glider,bounds=bounds)
surfaces.map(fig=fig,ax=axes[0],var='time')

depth_plot = DepthPlot(instrument=glider,bounds=bounds)

depth_plot.time_series(fig=fig,ax=axes[1],var='temperature')
depth_plot.var_var(fig=fig,ax=axes[2],var1='salinity',var2='temperature',color_var='depth')

plt.show()
