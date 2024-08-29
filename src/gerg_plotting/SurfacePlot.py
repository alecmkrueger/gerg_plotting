from attrs import define,field
import matplotlib.collections

from gerg_plotting.Plotter import Plotter
from gerg_plotting.SpatialInstruments import Bathy


@define
class SurfacePlot(Plotter):
    bathy:Bathy = field(init=False)
    sc:matplotlib.collections.PathCollection = field(init=False)

    def __attrs_post_init__(self):
        self.init_bathy()

    def init_bathy(self):
        self.bathy = Bathy(bounds=self.bounds)

    def map(self,var:str|None=None,pointsize=3,fig=None,ax=None) -> None:
        self.init_figure(fig,ax)
        if var is None:
            color = 'k'
            cmap = None
        else:
            color_var_values = self.instrument[var].copy()
            color = color_var_values
            cmap = self.get_cmap(var)
        if self.bounds is not None:
            self.ax.set_ylim(self.bounds.lat_min,self.bounds.lat_max)
            self.ax.set_xlim(self.bounds.lon_min,self.bounds.lon_max)

        # Add Bathymetry
        self.ax.contourf(self.bathy.lon,self.bathy.lat,self.bathy.depth,levels=self.bathy.contour_levels,cmap=self.bathy.cmap,vmin=self.bathy.vmin)
        # Add Scatter points
        self.sc = self.ax.scatter(self.instrument.lon,self.instrument.lat,c=color,cmap=cmap,s=pointsize)
        print(var)
        self.add_colorbar(self.sc,var)
        self.ax.set_ylabel('Latitude')
        self.ax.set_xlabel('Longitude')

    def quiver(self) -> None:
        # self.init_figure()
        raise NotImplementedError('Need to add Quiver')