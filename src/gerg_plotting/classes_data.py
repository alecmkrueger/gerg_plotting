import numpy as np
from attrs import define,field,asdict,validators
import matplotlib
from matplotlib.colors import Colormap
import cmocean
from pprint import pformat
import xarray as xr
from pathlib import Path

from gerg_plotting.classes_utils import get_center_of_mass,lat_min_smaller_than_max,lon_min_smaller_than_max

@define
class NonSpatialData:
    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)

class Lab(NonSpatialData):
    def __init__(self,vars):
        for key,value in vars.items():
            setattr(self,key,value)
    def __getitem__(self, key:str):
        return getattr(self,key)
    def __setitem__(self,key,value):
        return setattr(self,key,value)
    def __repr__(self):
        '''Pretty printing'''
        return pformat(self.__dict__, indent=1,width=2,compact=True,depth=1)

@define
class Bounds(NonSpatialData):
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)


@define
class SpatialData:
    # Dims
    lat:np.ndarray = field(default=None)
    lon:np.ndarray = field(default=None)
    depth:np.ndarray = field(default=None)
    time:np.ndarray = field(default=None)
    # Cmaps
    temperature_cmap:Colormap = field(default=cmocean.cm.thermal)
    salinity_cmap:Colormap = field(default=cmocean.cm.haline)
    u_current_cmap:Colormap = field(default=cmocean.cm.delta)
    v_current_cmap:Colormap = field(default=cmocean.cm.delta)

    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)

@define
class Bathy(SpatialData):
    # Vars
    bounds:Bounds = field(default=None)
    resolution_level:float|int|None = field(default=5)
    cmap:Colormap = field(default=matplotlib.cm.get_cmap('Blues'))
    vertical_scaler:int|float = field(default=None)
    vertical_units:str = field(default='')
    center_of_mass:tuple = field(init=False)

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

        # seafloor_path = Path('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        self_path = Path(__file__)
        seafloor_path = self_path.joinpath('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        self.depth = ds['elevation'].values*-1 #extract the depth values and flip them

        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting


@define
class Glider(SpatialData):
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray = field(default=None)

@define
class Buoy(SpatialData):
    # Vars
    u_current:np.ndarray = field(default=None)
    v_current:np.ndarray = field(default=None)

@define
class CTD(SpatialData):
    # Dim
    stations:np.ndarray = field(default=None)
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray = field(default=None)

@define
class WaveGlider(SpatialData):
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray  = field(default=None)
    
@define
class Radar(SpatialData):
    u_current:np.ndarray = field(default=None)
    v_current:np.ndarray = field(default=None)