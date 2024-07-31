import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from plotting.plotter_classes2d import SurfacePlot,DepthPlot,Histogram
from plotting.classes_data import Buoy, Glider,CTD,Bounds
from plotting.utils_plotter2d import filter_var

ds = xr.open_dataset('../test_data/buoy.nc')
ds = ds.sel(date=slice('2020-12-15',None))
df = ds[['u','v']].to_dataframe().reset_index()
cutoff_value=75
df['u'] = filter_var(df['u'],min_value=-cutoff_value,max_value=cutoff_value)
df['v'] = filter_var(df['v'],min_value=-cutoff_value,max_value=cutoff_value)

buoy = Buoy(lat = np.array([21]),
            lon = np.array([-85]),
            depth= df['bin'].to_numpy(),
            time = df['date'].to_numpy(),
            u_current=df['u'].to_numpy(),
            v_current=df['v'].to_numpy())

bounds = Bounds(lat_min=18,
                lat_max=24,
                lon_max=-82,
                lon_min=-89,
                depth_bottom=1000,
                depth_top=None)

fig,axes = plt.subplots(nrows=4,figsize = (5,20))
hist = Histogram(instrument=buoy,bounds=bounds)
hist.plot(fig=fig,ax=axes[0],var='u_current')
# plt.show()
hist.plot(fig=fig,ax=axes[1],var='v_current')
# plt.show()
hist.plot2d(fig=fig,ax=axes[2],x='u_current',y='v_current',bins=150,range=[[-cutoff_value, cutoff_value], [-cutoff_value, cutoff_value]],norm='log')
hist.ax.invert_yaxis()
# plt.show()
hist.plot3d(fig=fig,ax=axes[3],x='u_current',y='v_current',bins=150,range=[[-cutoff_value, cutoff_value], [-cutoff_value, cutoff_value]])
plt.show()
