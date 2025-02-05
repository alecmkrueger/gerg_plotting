from attrs import define, field
import matplotlib.colorbar
import matplotlib.collections
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.axes_divider import AxesDivider
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.gridliner
import cmocean
import numpy as np

from gerg_plotting.plotting_classes.plotter import Plotter
from gerg_plotting.data_classes.bathy import Bathy


@define
class MapPlot(Plotter):
    """
    A class for plotting geographic data on maps using Cartopy and Matplotlib.

    Parameters
    ----------
    bathy : Bathy, optional
        Bathymetric data object
    grid_spacing : int, optional
        Spacing between gridlines in degrees, default is 1

    Attributes
    ----------
    sc : matplotlib.collections.PathCollection
        Scatter plot collection
    gl : cartopy.mpl.gridliner.Gridliner
        Gridliner for map coordinates
    cbar_var : matplotlib.colorbar.Colorbar
        Colorbar for plotted variable
    cbar_bathy : matplotlib.colorbar.Colorbar
        Colorbar for bathymetry
    """
    
    bathy: Bathy = field(default=None)  # Bathymetry data object
    sc: matplotlib.collections.PathCollection = field(init=False)  # Scatter plot collection
    gl: cartopy.mpl.gridliner.Gridliner = field(init=False)  # Gridliner for controlling map gridlines
    cbar_var: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for the variable being plotted
    cbar_bathy: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for bathymetry data
    grid_spacing: int = field(default=1)  # Spacing of the gridlines on the map in degrees

    _quiver_density: int = field(default=None)  # Density of quiver plot
    _show_grid: bool = field(default=True)  # Whether to show gridlines on the map
    _show_coords: bool = field(default=True)  # Whether to show coordinates on the map
    

    @property
    def quiver_step(self):
        """Step size for quiver plot density based on data length"""
        if self._quiver_density is not None:
            return round(len(self.data.u.values)/self._quiver_density)
        return None

    @property 
    def bathy_initialized(self):
        """Check if bathymetry is properly initialized"""
        return isinstance(self.bathy, Bathy)

    @property
    def map_extent(self):
        """Get map extent from data bounds"""
        if self.data.bounds is not None:
            return [
                self.data.bounds.lon_min,
                self.data.bounds.lon_max,
                self.data.bounds.lat_min, 
                self.data.bounds.lat_max
            ]
        return None

    @property
    def gridlines(self):
        """Configure and return gridlines based on current settings"""
        gl = self.ax.gridlines(
            draw_labels=True,
            linewidth=1,
            color='gray',
            alpha=0.4 if self._show_grid else 0.0,
            linestyle='--'
        )
        gl.xlocator = MultipleLocator(self.grid_spacing)
        gl.ylocator = MultipleLocator(self.grid_spacing)
        return gl

    @property 
    def coordinate_labels(self):
        """Configure coordinate label formatting"""
        self.gl.top_labels = False
        self.gl.right_labels = False
        
        if self._show_coords:
            self.gl.xformatter = LONGITUDE_FORMATTER
            self.gl.yformatter = LATITUDE_FORMATTER
        else:
            self.gl.bottom_labels = False
            self.gl.left_labels = False


    def _init_bathy(self) -> None:
        """
        Initialize bathymetry object based on map bounds.

        Creates a new Bathy object if none exists, using current map bounds.
        """
        if not isinstance(self.bathy, Bathy):
            self.bathy = Bathy(bounds=self.data.bounds)
            
    def get_color_settings(self, var: str | None) -> tuple[str | np.ndarray, Colormap]:
        """
        Get color and colormap settings for specified variable.
        
        Parameters
        ----------
        var : str or None
            Variable name for color mapping
            
        Returns
        -------
        tuple
            (color, cmap) where color is str or ndarray and cmap is Colormap
        """
        if var is None:
            return 'k', None
        
        if var == 'time':
            color = np.array(self.data.date2num())
        else:
            color = self.data[var].values.copy()
        
        return color, self.get_cmap(var)


    def _set_up_map(self, fig=None, ax=None, var=None) -> tuple[str,Colormap,AxesDivider]:
        self.init_figure(fig=fig, ax=ax, geography=True)
        
        color, cmap = self.get_color_settings(var)
        
        if self.data.bounds is not None:
            self.ax.set_extent(self.map_extent)
        
        divider = make_axes_locatable(self.ax)
        return color, cmap, divider


    def _add_coasts(self,show_coastlines) -> None:
        """
        Add coastlines to the map.

        Parameters
        ----------
        show_coastlines : bool
            Whether to display coastlines
        """
        if show_coastlines:
            self.ax.coastlines()

    def _get_quiver_step(self,quiver_density) -> int|None:
        """
        Calculate step size for quiver plot density.

        Parameters
        ----------
        quiver_density : int or None
            Desired density of quiver arrows

        Returns
        -------
        int or None
            Step size for data slicing
        """
        if quiver_density is not None:
            step = round(len(self.data.u.values)/quiver_density)
        else:
            step = None
        return step


    def _add_grid(self, grid:bool, show_coords:bool=True) -> None:
        # Use gridlines property
        self.gl = self.gridlines
        
        # Configure labels using coordinate_labels property
        self.coordinate_labels

    def _add_bathy(self, show_bathy, divider) -> None:
        """
        Add bathymetric contours to map.

        Parameters
        ----------
        show_bathy : bool
            Whether to display bathymetry
        divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider
            Divider for colorbar placement
        """
        if show_bathy:
            self._init_bathy()
            bathy_contourf = self.ax.contourf(self.bathy.lon, self.bathy.lat, self.bathy.depth,
                                              levels=self.bathy.contour_levels, cmap=self.bathy.cmap,
                                              vmin=self.bathy.vmin, transform=ccrs.PlateCarree(), extend='both')
            # Add a colorbar for the bathymetry
            self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf, divider=divider,
                                                      fig=self.fig, nrows=self.nrows)

    def scatter(self, var: str | None = None, show_bathy: bool = True, show_coastlines:bool=True, pointsize=3, 
                linewidths=0, grid=True,show_coords=True, fig=None, ax=None) -> None:
        """
        Create scatter plot of points on map.

        Parameters
        ----------
        var : str or None, optional
            Variable name for color mapping
        show_bathy : bool, optional
            Whether to show bathymetry, default True
        show_coastlines : bool, optional
            Whether to show coastlines, default True
        pointsize : int, optional
            Size of scatter points, default 3
        linewidths : int, optional
            Width of point edges, default 0
        grid : bool, optional
            Whether to show grid, default True
        show_coords : bool, optional
            Whether to show coordinates, default True
        fig : matplotlib.figure.Figure, optional
            Figure to plot on
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        """
        color, cmap, divider = self._set_up_map(fig=fig, ax=ax, var=var)
        

        # Add bathymetry if needed
        self._add_bathy(show_bathy, divider)
        
        # Plot scatter points on the map
        self.sc = self.ax.scatter(self.data['lon'].values, self.data['lat'].values, linewidths=linewidths,
                                  c=color, cmap=cmap, s=pointsize, transform=ccrs.PlateCarree(),vmin=self.data[var].vmin,vmax=self.data[var].vmax)
        # Add a colorbar for the scatter plot variable
        self.cbar_var = self.add_colorbar(self.sc, var, divider, total_cbars=(2 if show_bathy else 1))

        self._add_coasts(show_coastlines)  # Add coastlines
        
        self._add_grid(grid=grid,show_coords=show_coords)


    def quiver(self,x:str='lon',y:str='lat',quiver_density:int=None,quiver_scale:float=None,grid:bool=True,show_bathy:bool=True,show_coastlines:bool=True,fig=None,ax=None) -> None:
        """
        Create quiver plot for vector data.

        Parameters
        ----------
        x : str, optional
            X-axis variable name, default 'lon'
        y : str, optional
            Y-axis variable name, default 'lat'
        quiver_density : int, optional
            Density of quiver arrows
        quiver_scale : float, optional
            Scaling factor for arrow length
        grid : bool, optional
            Whether to show grid, default True
        show_bathy : bool, optional
            Whether to show bathymetry, default True
        show_coastlines : bool, optional
            Whether to show coastlines, default True
        fig : matplotlib.figure.Figure, optional
            Figure to plot on
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        """
        # Set up the map
        _, cmap, divider = self._set_up_map(fig=fig, ax=ax, var='speed')
        
        # Use bathy_initialized property
        if self.bathy_initialized:
            self._add_bathy(show_bathy, divider)

        # Use quiver_step property
        step = self.quiver_step

        mappable = self.ax.quiver(
            self.data[x].values[::step], 
            self.data[y].values[::step],
            self.data.u.values[::step], 
            self.data.v.values[::step],
            self.data.speed.values[::step], 
            cmap=cmap,
            pivot='tail', 
            scale=quiver_scale, 
            units='height'
        )
        
