import numpy as np
from attrs import define,field
import matplotlib
from matplotlib.colors import Colormap
import xarray as xr
from pathlib import Path
import cmocean

from gerg_plotting.utils import get_center_of_mass
from gerg_plotting.SpatialInstrument import SpatialInstrument
from gerg_plotting.NonSpatialInstruments import Bounds

@define
class Bathy(SpatialInstrument):
    # Vars
    bounds:Bounds = field(default=None)
    resolution_level:float|int|None = field(default=5)
    contour_levels:int = field(default=50)
    land_color:list = field(default=[231/255,194/255,139/255,1])
    vmin:int|float = field(default=0)
    cmap:Colormap = field(default=matplotlib.cm.get_cmap('Blues'))
    vertical_scaler:int|float = field(default=None)
    vertical_units:str = field(default='')
    center_of_mass:tuple = field(init=False)

    def __attrs_post_init__(self):
        self.get_bathy()
        if self.vertical_scaler is not None:
            self.depth = self.depth*self.vertical_scaler
        self.center_of_mass = get_center_of_mass(self.lon,self.lat,self.depth)
        self.adjust_cmap()
        
    def adjust_cmap(self):
        # Remove the white most but of the colormap
        self.cmap = cmocean.tools.crop_by_percent(self.bathy.cmap,20,'min')
        # Add land color to the colormap
        self.cmap.set_under(self.bathy.land_color)

    def get_bathy(self):
        '''
        bounds (Bounds): contains attributes of lat_min,lon_min,lat_max,lon_max,depth_max,depth_min
        resolution_level (float|int): how much to coarsen the dataset by in units of degrees
        '''
        self_path = Path(__file__)
        seafloor_path = self_path.parent.joinpath('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
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
class Glider(SpatialInstrument):
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray = field(default=None)
    density:np.ndarray = field(default=None)
    mission:np.ndarray = field(default=None)

@define
class Buoy(SpatialInstrument):
    # Vars
    u_current:np.ndarray = field(default=None)
    v_current:np.ndarray = field(default=None)
    s_current:np.ndarray = field(default=None)

@define
class CTD(SpatialInstrument):
    # Dim
    stations:np.ndarray = field(default=None)
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray = field(default=None)

@define
class WaveGlider(SpatialInstrument):
    # Vars
    temperature:np.ndarray = field(default=None)
    salinity:np.ndarray  = field(default=None)
    
@define
class Radar(SpatialInstrument):
    u_current:np.ndarray = field(default=None)
    v_current:np.ndarray = field(default=None)
    s_current:np.ndarray = field(default=None)
