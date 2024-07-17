import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
# from plotter_classes import SurfacePlot,Glider,DepthPlot,Bounds,Histogram
from plotter_classes import SurfacePlot,DepthPlot,Histogram
from data_classes import Buoy, Glider,CTD
from bounds import Bounds
from utils.plotter_utils import interp_data,filter_var

ds = xr.open_dataset('../test_data/tabs225m01_K.nc')
ds = ds.sel(date=slice('2021',None))
df = ds[['e','v']].to_dataframe().reset_index()
df['e'] = filter_var(df['e'],min_value=-50,max_value=50)
df['v'] = filter_var(df['v'],min_value=-50,max_value=50)

buoy = Buoy(lat = np.array([21]),
            lon = np.array([-85]),
            depth= df['depth'].to_numpy(),
            time = df['date'].to_numpy(),
            u_current=df['e'].to_numpy(),
            v_current=df['v'].to_numpy())

bounds = Bounds(lat_min=18,
                lat_max=24,
                lon_max=-82,
                lon_min=-89,
                depth_bottom=1000,
                depth_top=None)

# fig,axes = plt.subplots(nrows=8,figsize = (10,35))
# surfaces = SurfacePlot(instrument=buoy,bounds=bounds)
# surfaces.map(fig=fig,ax=axes[0])
# surfaces.map(fig=fig,ax=axes[1],var='u_current',surface_values=False)
# surfaces.map(fig=fig,ax=axes[2],var='v_current',surface_values=False)

depth_plot = DepthPlot(instrument=buoy,bounds=bounds)

depth_plot.time_series(var='u_current')
plt.show()
depth_plot.time_series(var='v_current')
plt.show()

hist = Histogram(instrument=buoy,bounds=bounds)
hist.plot(var='u_current')
plt.show()
hist.plot(var='v_current')
plt.show()
hist.plot2d(x='u_current',y='v_current',bins=100,range=[[-100, 100], [-100, 100]],norm='log')
hist.ax.invert_yaxis()
plt.show()
