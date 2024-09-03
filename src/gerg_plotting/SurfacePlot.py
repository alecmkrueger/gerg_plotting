from attrs import define,field
import matplotlib.colorbar
import matplotlib.collections
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np

from gerg_plotting.Plotter import Plotter
from gerg_plotting.SpatialInstruments import Bathy


@define
class SurfacePlot(Plotter):
    bathy:Bathy = field(init=False)
    sc:matplotlib.collections.PathCollection = field(init=False)
    cbar_var:matplotlib.colorbar.Colorbar = field(init=False)
    cbar_bathy:matplotlib.colorbar.Colorbar = field(init=False)
    grid_spacing:int = field(default=1)

    def __attrs_post_init__(self):
        self.init_bathy()

    def init_bathy(self):
        self.bathy = Bathy(bounds=self.bounds)

    def map(self,var:str|None=None,pointsize=3,grid=True,fig=None,ax=None) -> None:
        self.init_figure(fig=fig,ax=ax,geography=True)
        if var is None:
            color = 'k'
            cmap = None
        else:
            color_var_values = self.instrument[var].copy()
            color = color_var_values
            cmap = self.get_cmap(var)
        if self.bounds is not None:
            self.ax.set_extent([self.bounds.lon_min,self.bounds.lon_max,
                               self.bounds.lat_min,self.bounds.lat_max])

        # Add Bathymetry
        bathy_contourf = self.ax.contourf(self.bathy.lon,self.bathy.lat,self.bathy.depth,
                                         levels=self.bathy.contour_levels,cmap=self.bathy.cmap,
                                         vmin=self.bathy.vmin,transform=ccrs.PlateCarree())
        self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf,ax=self.ax)
        # Add Scatter points
        self.sc = self.ax.scatter(self.instrument.lon,self.instrument.lat,
                                  c=color,cmap=cmap,s=pointsize,transform=ccrs.PlateCarree())
        self.cbar_var = self.add_colorbar(self.sc,var)
        if grid:
            gl = self.ax.gridlines(draw_labels=True,linewidth=1, color='gray', 
                                alpha=0.4, linestyle='--')
            gl.top_labels = False
            gl.right_labels = False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER


    def quiver(self) -> None:
        # self.init_figure()
        raise NotImplementedError('Need to add Quiver')