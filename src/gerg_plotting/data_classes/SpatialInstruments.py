import matplotlib.figure
import numpy as np
import math
import pandas as pd
from attrs import define,field,asdict
import matplotlib
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.colorbar
from matplotlib.colors import Colormap
import xarray as xr
from pathlib import Path
import cmocean
from typing import Iterable
from scipy.signal import welch


from gerg_plotting.modules.calculations import get_center_of_mass,rotate_vector
from gerg_plotting.modules.filters import filter_nan
from gerg_plotting.modules.plotting import colorbar
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.Bounds import Bounds
from gerg_plotting.data_classes.Variable import Variable

@define(repr=False)
class Bathy(SpatialInstrument):
    # Vars
    bounds:Bounds = field(default=None)
    resolution_level:float|int|None = field(default=5)
    contour_levels:int = field(default=50)
    land_color:list = field(default=[231/255,194/255,139/255,1])
    vmin:int|float = field(default=0)
    cmap:Colormap = field(default=matplotlib.colormaps.get_cmap('Blues'))
    cbar_show:bool = field(default=True)
    cbar:matplotlib.colorbar.Colorbar = field(init=False)
    cbar_nbins:int = field(default=5)
    cbar_kwargs:dict = field(default={})
    vertical_scaler:int|float = field(default=None)
    vertical_units:str = field(default='')
    center_of_mass:tuple = field(init=False)
    label:str = field(default='Bathymetry')

    def __attrs_post_init__(self):
        self.get_bathy()
        if self.vertical_scaler is not None:
            self.depth = self.depth*self.vertical_scaler
        self.center_of_mass = get_center_of_mass(self.lon,self.lat,self.depth)
        self.adjust_cmap()

    def get_label(self):
        if self.vertical_units != '':
            self.label = f"Bathymetry ({self.vertical_units})"
        return self.label
        
    def adjust_cmap(self):
        # Remove the white most but of the colormap
        self.cmap = cmocean.tools.crop_by_percent(self.cmap,20,'min')
        # Add land color to the colormap
        self.cmap.set_under(self.land_color)

    def get_bathy(self):
        '''
        bounds (Bounds): contains attributes of lat_min,lon_min,lat_max,lon_max,depth_max,depth_min
        resolution_level (float|int): how much to coarsen the dataset by in units of degrees

        returns:
        lon,lat,depth
        '''
        self_path = Path(__file__).parent
        seafloor_path = self_path.parent.joinpath('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        self.depth = ds['elevation'].values*-1 #extract the depth values and flip them
    
        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting

        return self.lon,self.lat,self.depth
    
    def add_colorbar(self,fig:matplotlib.figure.Figure,divider,mappable:matplotlib.axes.Axes,nrows:int) -> None:
        if self.cbar_show:
            label = 'Bathymetry (m)'
            self.cbar = colorbar(fig,divider,mappable,label,nrows=nrows)
            self.cbar.ax.locator_params(nbins=self.cbar_nbins)
            self.cbar.ax.invert_yaxis()
            return self.cbar


@define(slots=False,repr=False)
class Data(SpatialInstrument):
    # Vars
    temperature: Iterable|Variable|None = field(default=None)
    salinity: Iterable|Variable|None = field(default=None)
    density: Iterable|Variable|None = field(default=None)
    u: Iterable|Variable|None = field(default=None)
    v: Iterable|Variable|None = field(default=None)
    w: Iterable|Variable|None = field(default=None)
    speed: Iterable|Variable|None = field(default=None)

    # Bounds
    bounds:Bounds = field(default=None)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._init_variables()  # Init variables

    def _init_variables(self):
        '''Default Variable initialization.
        If you would like a new variable to be included in the default init, contact the repo manager'''
        self._init_variable(var='temperature', cmap=cmocean.cm.thermal, units='°C', vmin=-10, vmax=40)
        self._init_variable(var='salinity', cmap=cmocean.cm.haline, units=None, vmin=28, vmax=40)
        self._init_variable(var='density', cmap=cmocean.cm.dense, units="kg/m\u00B3", vmin=1020, vmax=1035)
        self._init_variable(var='u', cmap=cmocean.cm.balance, units="m/s", vmin=-5, vmax=5)
        self._init_variable(var='v', cmap=cmocean.cm.balance, units="m/s", vmin=-5, vmax=5)
        self._init_variable(var='w', cmap=cmocean.cm.balance, units="m/s", vmin=-5, vmax=5)
        self._init_variable(var='speed', cmap=cmocean.cm.speed, units="m/s", vmin=0, vmax=5)

    def calculate_speed(self,include_w:bool=False):
        if self.speed is None:
            if include_w:
                if self.check_for_vars(['u','v','w']):
                    self.speed = math.hypot(self.u.data,self.v.data,self.w.data)
                    self._init_variable(var='speed', cmap=cmocean.cm.speed, units="m/s", vmin=0, vmax=5)  
            if self.check_for_vars(['u','v']):
                self.speed = math.hypot(self.u.data,self.v.data)
                self._init_variable(var='speed', cmap=cmocean.cm.speed, units="m/s", vmin=0, vmax=5)

    def calcluate_PSD(self,sampling_freq,segment_length,theta_rad=None):
        '''
        Calculate the power spectral density using Welch's method

        segment_length (int): Length of each segment for Welch's method
        '''

        u = self.u.data
        v = self.v.data
        if self.w is not None:
            w = self.w.data
        else:
            w = None

        # Rotate vectors if needed
        if theta_rad is not None:
            u,v = rotate_vector(u,v,theta_rad)

        # Filter out NaNs
        u = filter_nan(u)
        v = filter_nan(v)
        if w is not None:
            w = filter_nan(w)

        freq, psd_U = welch(u**2, fs=sampling_freq, nperseg=segment_length)
        _, psd_V = welch(v**2, fs=sampling_freq, nperseg=segment_length)
        if w is not None:
            _, psd_W = welch(w**2, fs=sampling_freq, nperseg=segment_length)

        # Register the new variables
        self.add_custom_variable(Variable(name='psd_freq',data=freq,cmap=cmocean.cm.thermal,units='cpd',label='Power Spectra Density Frequency (cpd)'),exist_ok=True)
        self.add_custom_variable(Variable(name='psd_u',data=psd_U,cmap=cmocean.cm.thermal,units='cm²/s²/cpd',label='Power Spectra Density U (cm²/s²/cpd)'),exist_ok=True)
        self.add_custom_variable(Variable(name='psd_v',data=psd_V,cmap=cmocean.cm.thermal,units='cm²/s²/cpd',label='Power Spectra Density V (cm²/s²/cpd)'),exist_ok=True)

        if w is None:
            return freq,psd_U,psd_V
        elif w is not None:
            self.add_custom_variable(Variable(name='psd_w',data=psd_W,cmap=cmocean.cm.thermal,units='cm²/s²/cpd',label='Power Spectra Density W (cm²/s²/cpd)'),exist_ok=True)
            return freq,psd_U,psd_V,psd_W




