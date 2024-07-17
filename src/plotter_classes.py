import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from attrs import define, field, asdict,validators
from pprint import pformat
from pathlib import Path
import xarray as xr
import cmocean

from utils.class_utils import lat_min_smaller_than_max,lon_min_smaller_than_max,get_center_of_mass


@define
class Bounds:
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)

    longitude_state:str = field(init=False)


    def relative_longitude(self):
        
        if self.lon_min is not None:
            self.lon_min = self.lon_min-360
        if self.lon_max is not None:
            self.lon_max = self.lon_max-360
        self.longitude_state = 'relative'

    def absoloute_longitude(self):
        if self.lon_min is not None:
            self.lon_min = self.lon_min+360
        if self.lon_max is not None:
            self.lon_max = self.lon_max+360
        self.longitude_state = 'absolute'

    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)
    def __getitem__(self, key:str):
        return asdict(self)[key]
    

@define
class Bathy:
    '''
    cmap: colormap object
    vertical_scalar: value to multiply the depth by
    '''
    bounds:Bounds
    resolution_level:float|int|None = field(default=5)
    cmap:None = field(default=None)
    vertical_scaler:int|float = field(default=None)
    vertical_units:str = field(default='')
    center_of_mass:tuple = field(init=False)
    lon:np.ndarray = field(init=False)
    lat:np.ndarray = field(init=False)
    depth:np.ndarray = field(init=False)

    def __attrs_post_init__(self):
        self.get_bathy()
        if self.vertical_scaler is not None:
            self.depth = self.depth*self.vertical_scaler
        self.center_of_mass = get_center_of_mass(self.lon,self.lat,self.depth)

    def get_bathy(self):
        '''
        bounds (Bounds): contains attributes of lat_min,lon_min,lat_max,lon_max,depth_max,depth_min
        resolution_level (float|int): how much to coarsen the dataset by in units of degrees
        '''
        seafloor_path = Path('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        self.depth = ds.elevation.values*-1 #extract the depth values
        # self.depth[np.isnan(self.depth)] = 0 #set all nan depth values to zero, makes land zero and flat to focus on bathymetry

        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting


    def __repr__(self):
        '''
        Pretty printing
        '''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)
    def __getitem__(self, key:str):
        return asdict(self)[key]


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

    fig:matplotlib.figure.Figure = field(default=None)
    ax:matplotlib.axes.Axes = field(default=None)

    def init_figure(self,fig=None,ax=None):
        if fig is None and ax is None:
            self.fig,self.ax = matplotlib.pyplot.subplots()
        elif fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax

@define
class SurfacePlot(Plotter):
    bathy:Bathy = field(init=False)

    def init_bathy(self):
        self.bathy = Bathy(self.bounds,resolution_level=5,cmap=matplotlib.cm.get_cmap('Blues'))

    def map(self,var:str|None=None,fig=None,ax=None,seafloor=True):
        self.init_figure(fig,ax)

        if var is None:
            color = 'k'            
        else:
            color = self.instrument[var]
        if self.bounds is not None:
            self.bounds.relative_longitude()
            self.ax.set_ylim(self.bounds.lat_min,self.bounds.lat_max)
            self.ax.set_xlim(self.bounds.lon_min,self.bounds.lon_max)
        if seafloor:
            self.init_bathy()
            # Remove the white most but of the colormap
            self.bathy.cmap = cmocean.tools.crop_by_percent(self.bathy.cmap,20,'min')
            # Add land color to the colormap
            land_color = [231/255,194/255,139/255,1]
            self.bathy.cmap.set_under(land_color)
            self.ax.contourf(self.bathy.lon,self.bathy.lat,self.bathy.depth,levels=50,cmap=self.bathy.cmap,vmin=0)
        self.ax.scatter(self.instrument.lon,self.instrument.lat,c=color)


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


    def var_var(self,x:str,y:str,color_var:str|None=None,fig=None,ax=None):
        self.init_figure(fig,ax)
        if color_var is not None:
            self.ax.scatter(self.instrument[x],self.instrument[y],c=self.instrument[color_var])
        elif color_var is None:
            self.ax.scatter(self.instrument[x],self.instrument[y])

    def cross_section(self,longitude,latitude):
        raise NotImplementedError('Need to add method to plot cross sections')

@define
class Histogram(Plotter):

    def plot(self,var:str,fig=None,ax=None):
        self.init_figure(fig,ax)
        self.ax.hist(self.instrument[var])

    def plot2d(self,x:str,y:str,fig=None,ax=None,**kwargs):
        self.init_figure(fig,ax,)
        self.ax.hist2d(self.instrument[x],self.instrument[y],**kwargs)