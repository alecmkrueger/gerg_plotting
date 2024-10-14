from attrs import define,field
import matplotlib.colorbar
import matplotlib.collections
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.gridliner

from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.data_classes.SpatialInstruments import Bathy


@define
class MapPlot(Plotter):
    '''
    
    '''
    bathy:Bathy = field(default=None)
    sc:matplotlib.collections.PathCollection = field(init=False)
    gl:cartopy.mpl.gridliner.Gridliner = field(init=False)
    cbar_var:matplotlib.colorbar.Colorbar = field(init=False)
    cbar_bathy:matplotlib.colorbar.Colorbar = field(init=False)
    grid_spacing:int = field(default=1)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.init_bathy()

    def init_bathy(self):
        if not isinstance(self.bathy,Bathy):
            self.bathy = Bathy(bounds=self.bounds)

    def set_up_map(self,fig,ax,var):
        self.init_figure(fig=fig,ax=ax,geography=True)
        if var is None:
            color = 'k'
            cmap = None
        else:
            color_var_values = self.instrument[var].data.copy()
            color = color_var_values
            cmap = self.get_cmap(var)
        if self.bounds is not None:
            self.ax.set_extent([self.bounds.lon_min,self.bounds.lon_max,
                               self.bounds.lat_min,self.bounds.lat_max])
        divider = make_axes_locatable(self.ax)
        return color,cmap,divider
    
    def add_coasts(self):
        self.ax.coastlines()

    def add_bathy(self,show_bathy,divider):
        # Add Bathymetry
        if show_bathy:
            bathy_contourf = self.ax.contourf(self.bathy.lon,self.bathy.lat,self.bathy.depth,
                                            levels=self.bathy.contour_levels,cmap=self.bathy.cmap,
                                            vmin=self.bathy.vmin,transform=ccrs.PlateCarree(),extend='both')
            self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf,divider=divider,fig=self.fig,nrows=self.nrows)

    def scatter(self,var:str|None=None,show_bathy:bool=True,pointsize=3,linewidths=0,grid=True,fig=None,ax=None) -> None:
        color,cmap,divider = self.set_up_map(fig,ax,var)

        self.add_bathy(show_bathy,divider)
        # Add Scatter points
        self.sc = self.ax.scatter(self.instrument['lon'].data,self.instrument['lat'].data, linewidths=linewidths,
                                  c=color,cmap=cmap,s=pointsize,transform=ccrs.PlateCarree())
        self.cbar_var = self.add_colorbar(self.sc,var,divider,total_cbars=(2 if show_bathy else 1))

        self.add_coasts()
        
        if grid:
            self.gl = self.ax.gridlines(draw_labels=True,linewidth=1, color='gray', 
                                alpha=0.4, linestyle='--')
            self.gl.top_labels = False
            self.gl.right_labels = False
            self.gl.xformatter = LONGITUDE_FORMATTER
            self.gl.yformatter = LATITUDE_FORMATTER
            self.gl.xlocator = MultipleLocator(self.grid_spacing)
            self.gl.ylocator = MultipleLocator(self.grid_spacing)


    def quiver(self) -> None:
        # self.init_figure()
        raise NotImplementedError('Need to add Quiver')