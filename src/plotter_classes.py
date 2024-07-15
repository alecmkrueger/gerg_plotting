import matplotlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from attrs import define, field, asdict,validators
from pprint import pformat

from utils.class_utils import lat_min_smaller_than_max,lon_min_smaller_than_max


@define
class Bounds:
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)

    def relative_longitude(self):
        self.lon_min = self.lon_min-360
        self.lon_max = self.lon_max-360

    def absoloute_longitude(self):
        self.lon_min = self.lon_min+360
        self.lon_max = self.lon_max+360

    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)
    

@define
class Glider:
    # Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray
    def __getitem__(self, key:str):
        return asdict(self)[key]

@define
class Buoy:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray
    u_current:np.ndarray
    v_current:np.ndarray
    def __getitem__(self, key:str):
        return asdict(self)[key]

@define
class CTD:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray
    def __getitem__(self, key:str):
        return asdict(self)[key]

@define
class WaveGlider:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray 
    def __getitem__(self, key:str):
        return asdict(self)[key]
    
@define
class Plotter:
    instrument:Glider|Buoy|CTD|WaveGlider
    bounds:Bounds|None = field(default= None)

    fig:matplotlib.figure.Figure|None = field(default=None)
    ax:matplotlib.axes.Axes|None = field(default=None)

    def init_figure(self,fig=None,ax=None):
        if fig is None and ax is None:
            self.fig,self.ax = matplotlib.pyplot.subplots()
        elif fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax

@define
class SurfacePlot(Plotter):

    def map(self,var:str|None=None,fig=None,ax=None):
        self.init_figure(fig,ax)

        if var is None:
            color = 'k'            
        else:
            color = self.instrument[var]

        self.ax.scatter(self.instrument.lon,self.instrument.lat,c=color)
        if self.bounds is not None:
            self.bounds.relative_longitude()
            self.ax.set_ylim(self.bounds.lat_min,self.bounds.lat_max)
            self.ax.set_xlim(self.bounds.lon_min,self.bounds.lon_max)


@define
class DepthPlot(Plotter):

    def time_series(self,var:str,fig=None,ax=None):
        self.init_figure(fig,ax)
        self.ax.scatter(self.instrument.time,self.instrument.depth,c=self.instrument[var])
        self.ax.invert_yaxis()
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)

        self.ax.xaxis.set_major_locator(locator)
        self.ax.xaxis.set_major_formatter(formatter)
        matplotlib.pyplot.xticks(rotation=60, fontsize='small')


    def var_var(self,var1:str,var2:str,color_var:str|None=None,fig=None,ax=None):
        self.init_figure(fig,ax)
        if color_var is not None:
            self.ax.scatter(self.instrument[var1],self.instrument[var2],c=self.instrument[color_var])
        elif color_var is None:
            self.ax.scatter(self.instrument[var1],self.instrument[var2])

@define
class Histogram(Plotter):

    def plot(self,var:str,fig=None,ax=None):
        ''''''
        self.init_figure(fig,ax)
        self.ax.hist(self.instrument[var])


    def plot2d(self,var1:str,var2:str,fig=None,ax=None):
        ''''''
        self.init_figure(fig,ax,)
        self.ax.hist2d(self.instrument[var1],self.instrument[var2])