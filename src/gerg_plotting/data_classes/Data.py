import math
from attrs import define,field
import cmocean
from typing import Iterable
from scipy.signal import welch

from gerg_plotting.modules.calculations import rotate_vector
from gerg_plotting.modules.filters import filter_nan
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.Bounds import Bounds
from gerg_plotting.data_classes.Variable import Variable


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