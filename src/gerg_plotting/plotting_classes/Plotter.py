import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.colorbar
import matplotlib.colorbar
import matplotlib.figure
import matplotlib.pyplot
from matplotlib.colors import Colormap
import matplotlib.dates as mdates
from attrs import define, field, asdict
from pprint import pformat
import cartopy.crs as ccrs

from gerg_plotting.data_classes.NonSpatialInstruments import NonSpatialInstrument,Variable
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.NonSpatialInstruments import Bounds
from gerg_plotting.utils import calculate_range,calculate_pad

@define
class Plotter:
    instrument:SpatialInstrument
    bounds:Bounds|None = field(default=None)
    bounds_padding:float = field(default=0.3)

    fig:matplotlib.figure.Figure = field(default=None)
    ax:matplotlib.axes.Axes = field(default=None)

    cbar_show:bool = field(default=True)
    cbar:matplotlib.colorbar.Colorbar = field(init=False)
    # cbar_shrink:float = field(default=1)
    cbar_nbins:int = field(default=5)
    # cbar_pad:float = field(default=0.05)
    cbar_kwargs:dict = field(default={})

    def __attrs_post_init__(self):
        self.detect_bounds()


    def init_figure(self, fig=None, ax=None, three_d=False, geography=False) -> None:
        '''Initalize the figure and axes if they are not provided'''
        
        # Guard clause: Ensure three_d and geography are not both True
        if three_d and geography:
            raise ValueError("Cannot set both 'three_d' and 'geography' to True. Choose one.")

        if fig is None and ax is None:
            if geography:
                # Initialize a figure with Cartopy's PlateCarree projection
                self.fig, self.ax = matplotlib.pyplot.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
            elif three_d:
                # Initialize a 3D figure
                self.fig, self.ax = matplotlib.pyplot.subplots(subplot_kw={'projection': '3d'})
            else:
                # Standard 2D Matplotlib figure with no projection
                self.fig, self.ax = matplotlib.pyplot.subplots()
        elif fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax
            if three_d:
                index = [idx for idx, ax in enumerate(self.fig.axes) if ax is self.ax][0] + 1
                self.ax.remove()
                gs = self.ax.get_gridspec()
                self.ax = fig.add_subplot(gs.nrows, gs.ncols, index, projection='3d')


    def detect_bounds(self) -> None:
        if isinstance(self.instrument,SpatialInstrument):
            if self.bounds is None:
                if isinstance(self.instrument.lat,Variable) | isinstance(self.instrument.lon,Variable):
                    lat_min,lat_max = calculate_pad(self.instrument.lat.data,pad=self.bounds_padding)
                    lon_min,lon_max = calculate_pad(self.instrument.lon.data,pad=self.bounds_padding)
                    _,depth_max = calculate_range(self.instrument.depth.data)
                    self.bounds = Bounds(lat_min=lat_min,
                                        lat_max=lat_max,
                                        lon_min=lon_min,
                                        lon_max=lon_max,
                                        depth_bottom=depth_max,
                                        depth_top=None)
                else:
                    raise ValueError(f'lat and lon must be of type Variable, you passed {type(self.instrument.lat) = } and {type(self.instrument.lon) = }')
        else:
            raise ValueError(f'Must pass an instrument of type SpatialInstrument, you passed {type(self.instrument) = }')

    def get_cmap(self,color_var:str) -> Colormap:
        # If there is a colormap for the provided color_var
        if self.instrument[color_var].cmap is not None:
            cmap = self.instrument[color_var].cmap
        # If there is no colormap for the provided color_var
        else:
            cmap = matplotlib.pyplot.get_cmap('viridis')
        return cmap
    
    def add_colorbar(self,mappable:matplotlib.axes.Axes,var:str|None) -> None:
        if self.cbar_show:
            if var is not None:
                cbar_label = self.instrument[var].get_label()
                self.cbar = matplotlib.pyplot.colorbar(mappable,ax=self.ax,
                                                label=cbar_label,**self.cbar_kwargs)
                self.cbar.ax.locator_params(nbins=self.cbar_nbins)
                if var == 'time':
                    self.cbar.ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

                # self.cbar.ax.invert_yaxis()
                return self.cbar

    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)