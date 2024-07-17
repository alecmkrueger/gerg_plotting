import numpy as np
from attrs import define,field,asdict
import matplotlib
from matplotlib.colors import Colormap
import cmocean
from pprint import pformat
import xarray as xr
from pathlib import Path

from utils.class_utils import validate_array_lengths,get_center_of_mass
from bounds import Bounds


@define
class Data:
    # Dims
    lat:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    lon:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    depth:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    time:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    # Cmaps
    temperature_cmap:Colormap = field(default=cmocean.cm.thermal)
    salinity_cmap:Colormap = field(default=cmocean.cm.haline)

    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)

@define
class Bathy(Data):
    '''
    cmap: colormap object
    vertical_scalar: value to multiply the depth by
    '''
    bounds:Bounds
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
        seafloor_path = Path('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        self.depth = ds.elevation.values*-1 #extract the depth values and flip them

        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting


@define
class Glider(Data):
    # Vars
    temperature:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    salinity:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)

@define
class Buoy(Data):
    # Vars
    temperature:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    salinity:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    u_current:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    v_current:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)

@define
class CTD(Data):
    # Vars
    temperature:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    salinity:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)

@define
class WaveGlider(Data):
    # Vars
    temperature:np.ndarray = field(factory=np.ndarray,validator=validate_array_lengths)
    salinity:np.ndarray  = field(factory=np.ndarray,validator=validate_array_lengths)
    