
import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
from plotter_classes import SurfacePlot,DepthPlot,Histogram
from data_classes import Buoy, Glider,CTD
from bounds import Bounds
from utils.plotter_utils import interp_data,filter_var

ds = xr.open_dataset('../test_data/2024_mission_44.nc')

df = interp_data(ds)

df['salinity'] = filter_var(df['salinity'],30,40)


df = df.where(df.time>pd.to_datetime('2024-01-01'))
df. dropna()
df = df[::100]


temperature = df['temperature'].to_numpy()
salinity = df['salinity'].to_numpy()
latitude = df['latitude'].to_numpy()
longitude = df['longitude'].to_numpy()
depth = df['pressure'].to_numpy()
dates = df['time'].to_numpy()


glider = Glider(lat = latitude,
                lon = longitude,
                depth = depth,
                time = dates,
                temperature = temperature,
                salinity = salinity)

bounds = Bounds(lat_min=18,
                lat_max=24,
                lon_max=-82,
                lon_min=-89,
                depth_bottom=1000,
                depth_top=None)

fig,axes = plt.subplots(nrows=8,figsize = (10,35))
surfaces = SurfacePlot(instrument=glider,bounds=bounds)
surfaces.map(fig=fig,ax=axes[0])
surfaces.map(fig=fig,ax=axes[1],var='temperature',surface_values=True)

depth_plot = DepthPlot(instrument=glider,bounds=bounds)

depth_plot.time_series(fig=fig,ax=axes[2],var='temperature')
depth_plot.var_var(fig=fig,ax=axes[3],x='salinity',y='temperature',color_var='salinity')
depth_plot.var_var(fig=fig,ax=axes[4],x='temperature',y='depth',color_var='salinity')
axes[4].invert_yaxis()

hist = Histogram(instrument=glider,bounds=bounds)
hist.plot(fig=fig,ax=axes[5],var='temperature')
hist.plot(fig=fig,ax=axes[6],var='salinity')
hist.plot2d(fig=fig,ax=axes[7],x='temperature',y='depth',range=[[0, 35], [0, 1000]],bins=100,norm='log')
hist.ax.invert_yaxis()


plt.show()