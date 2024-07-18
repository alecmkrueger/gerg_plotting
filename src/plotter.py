import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
# from plotter_classes import SurfacePlot,Glider,DepthPlot,Bounds,Histogram
from plotter_classes import SurfacePlot,DepthPlot,Histogram
from data_classes import Radar
from bounds import Bounds
from utils.plotter_utils import interp_data,filter_var

radar = Radar()

bounds = Bounds(lat_min=27,
                lat_max=31,
                lon_max=-88,
                lon_min=-94,
                depth_bottom=1000,
                depth_top=None)

fig,axes = plt.subplots(nrows=3,figsize = (10,10))
surfaces = SurfacePlot(instrument=radar,bounds=bounds)
surfaces.map(fig=fig,ax=axes[0])
surfaces.map(fig=fig,ax=axes[1],var='temperature',surface_values=False)
surfaces.map(fig=fig,ax=axes[2],var='salinity',surface_values=False)
plt.show()

depth_plot = DepthPlot(instrument=radar,bounds=bounds)

depth_plot.time_series(var='temperature')
plt.show()
depth_plot.time_series(var='salinity')
plt.show()
depth_plot.var_var(x='salinity',y='temperature',color_var='depth')
plt.show()

fig,axes = plt.subplots(nrows=4,figsize = (5,20))
hist = Histogram(instrument=radar,bounds=bounds)
hist.plot(fig=fig,ax=axes[0],var='temperature')
# plt.show()
hist.plot(fig=fig,ax=axes[1],var='salinity')
# plt.show()
hist.plot2d(fig=fig,ax=axes[2],x='temperature',y='salinity',bins=150,norm='log')
hist.ax.invert_yaxis()
# plt.show()
hist.plot3d(fig=fig,ax=axes[3],x='temperature',y='salinity',bins=150)
plt.show()
