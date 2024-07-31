import numpy as np
import pandas as pd
import datetime
import xarray as xr
import matplotlib.pyplot as plt
from plotting.plotter_classes2d import SurfacePlot,DepthPlot,Histogram
from plotting.classes_data import Radar,Bounds
from plotting.utils_plotter2d import interp_data,filter_var,calculate_range

df = pd.read_csv('../test_data/radar.csv',
                 parse_dates=['time'],date_format='%Y-%m-%dT%H:%M:%SZ',skiprows=[1])

times = list(set(df.time))

df = df.loc[df.time==times[2]]

radar = Radar(lat=df['latitude'],
              lon=df['longitude'],
              depth=np.array([0]),
              time=df['time'],
              u_current=df['u'],
              v_current=df['v'])

lat_min,lat_max = calculate_range(radar.lat)
lon_min,lon_max = calculate_range(radar.lon)


bounds = Bounds(lat_min=lat_min,
                lat_max=lat_max,
                lon_max=lon_max,
                lon_min=lon_min,
                depth_bottom=1000,
                depth_top=None)


fig,axes = plt.subplots(nrows=3,figsize = (10,10))
surfaces = SurfacePlot(instrument=radar,bounds=bounds)
surfaces.map(fig=fig,ax=axes[0])
surfaces.map(fig=fig,ax=axes[1],var='u_current',surface_values=False)
surfaces.map(fig=fig,ax=axes[2],var='v_current',surface_values=False)
plt.show()

# depth_plot = DepthPlot(instrument=radar,bounds=bounds)

# depth_plot.time_series(var='u_current')
# plt.show()
# depth_plot.time_series(var='v_current')
# plt.show()
# depth_plot.var_var(x='v_current',y='u_current',color_var='time')
# plt.show()

fig,axes = plt.subplots(nrows=4,figsize = (5,20))
hist = Histogram(instrument=radar,bounds=bounds)
hist.plot(fig=fig,ax=axes[0],var='u_current')
# plt.show()
hist.plot(fig=fig,ax=axes[1],var='v_current')
# plt.show()
hist.plot2d(fig=fig,ax=axes[2],x='u_current',y='v_current',bins=150,norm='log')
hist.ax.invert_yaxis()
# plt.show()
hist.plot3d(fig=fig,ax=axes[3],x='u_current',y='v_current',bins=150)
plt.show()
