import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.colorbar
import matplotlib.figure
import matplotlib.pyplot
from matplotlib.colors import Colormap
from matplotlib.dates import DateFormatter, DayLocator
from attrs import define, field, asdict
from pprint import pformat

from gerg_plotting.NonSpatialInstruments import NonSpatialInstrument
from gerg_plotting.SpatialInstrument import SpatialInstrument
from gerg_plotting.NonSpatialInstruments import Bounds
from gerg_plotting.utils import calculate_range,calculate_pad

@define
class Plotter:
    instrument:NonSpatialInstrument|SpatialInstrument
    bounds:Bounds|None = field(default=None)
    bounds_padding:float = field(default=0.3)

    fig:matplotlib.figure.Figure = field(default=None)
    ax:matplotlib.axes.Axes = field(default=None)

    cbar:matplotlib.colorbar.Colorbar = field(init=False)
    colorbar_day_interval:int = field(default=5)
    colorbar_bins:int = field(default=5)

    def __attrs_post_init__(self):
        self.detect_bounds()

    def init_figure(self,fig=None,ax=None,three_d=False) -> None:
        '''Initalize the figure and axes if they are not provided'''
        if fig is None and ax is None:
            self.fig,self.ax = matplotlib.pyplot.subplots(subplot_kw={'projection':('3d' if three_d else None)})
        elif fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax
            if three_d:
                index = [idx for idx,ax in enumerate(self.fig.axes) if ax is self.ax][0]+1
                self.ax.remove()
                gs = self.ax.get_gridspec()
                self.ax = fig.add_subplot(gs.nrows,gs.ncols,index, projection='3d')

    def detect_bounds(self) -> None:
        if isinstance(self.instrument,SpatialInstrument):
            if self.bounds is None:
                if (self.instrument.lat is not None) | (self.instrument.lon is not None):
                    lat_min,lat_max = calculate_pad(self.instrument.lat,pad=self.bounds_padding)
                    lon_min,lon_max = calculate_pad(self.instrument.lon,pad=self.bounds_padding)
                    _,depth_max = calculate_range(self.instrument.depth)
                    self.bounds = Bounds(lat_min=lat_min,
                                        lat_max=lat_max,
                                        lon_min=lon_min,
                                        lon_max=lon_max,
                                        depth_bottom=depth_max,
                                        depth_top=None)

    def get_cmap(self,color_var:str) -> Colormap:
        # If there is a colormap for the provided color_var
        if self.instrument.cmaps.has_var(color_var):
            cmap = self.instrument.cmaps[color_var]
        # If there is no colormap for the provided color_var
        else:
            cmap = matplotlib.pyplot.get_cmap('viridis')
        return cmap
    
    def add_colorbar(self,mappable:matplotlib.axes.Axes,var:str|None) -> None:
        if var is not None:
            cbar_label = self.instrument.vars_with_units[var]
            if var == 'time':
                self.cbar = matplotlib.pyplot.colorbar(mappable,ax=self.ax,label=cbar_label,ticks=DayLocator(interval=self.colorbar_day_interval))
            else:
                self.cbar = matplotlib.pyplot.colorbar(mappable,ax=self.ax,label=cbar_label)
                self.cbar.ax.locator_params(nbins=self.colorbar_bins)
            # self.cbar.ax.invert_yaxis()

    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)
