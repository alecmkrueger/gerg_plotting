from attrs import define, field
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
    """
    A class for plotting geographic data on a map using Cartopy and Matplotlib.
    It provides functionality to plot bathymetry, scatter plots, and configure the map with coastlines, grids, and colorbars.
    
    Attributes:
    - bathy (Bathy): Object containing bathymetric data for the map.
    - sc (PathCollection): Matplotlib object for scatter plots.
    - gl (Gridliner): Object for managing gridlines on the map.
    - cbar_var (Colorbar): Colorbar for the variable being visualized (e.g., temperature, salinity).
    - cbar_bathy (Colorbar): Colorbar for the bathymetry.
    - grid_spacing (int): Spacing for the gridlines on the map (default is 1 degree).
    """
    
    bathy: Bathy = field(default=None)  # Bathymetry data object
    sc: matplotlib.collections.PathCollection = field(init=False)  # Scatter plot collection
    gl: cartopy.mpl.gridliner.Gridliner = field(init=False)  # Gridliner for controlling map gridlines
    cbar_var: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for the variable being plotted
    cbar_bathy: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for bathymetry data
    grid_spacing: int = field(default=1)  # Spacing of the gridlines on the map

    def __attrs_post_init__(self):
        """
        Post-initialization method. This is automatically called after the object is created.
        Calls the parent's post-init and initializes bathymetry if not provided.
        """
        super().__attrs_post_init__()
        self.init_bathy()

    def init_bathy(self):
        """
        Initializes the bathymetry object if it's not already provided.
        If no bathymetry object is passed, it creates one based on the current map bounds.
        """
        if not isinstance(self.bathy, Bathy):
            self.bathy = Bathy(bounds=self.bounds)

    def set_up_map(self, fig, ax, var):
        """
        Sets up the figure and axis for the map plot, including axis limits, color maps, and dividers for colorbars.
        
        Parameters:
        - fig (Figure): Matplotlib figure object.
        - ax (Axes): Matplotlib axes object for the map.
        - var (str | None): Variable name for color mapping (e.g., temperature, salinity).

        Returns:
        - color (str | np.ndarray): Color values for scatter plot points.
        - cmap (Colormap | None): Colormap for the scatter plot.
        - divider (AxesDivider): Divider object for placing colorbars.
        """
        self.init_figure(fig=fig, ax=ax, geography=True)
        
        if var is None:
            color = 'k'  # Use black color if no variable is provided
            cmap = None
        else:
            color_var_values = self.instrument[var].data.copy()
            color = color_var_values  # Color is determined by the variable data
            cmap = self.get_cmap(var)  # Get the appropriate colormap for the variable
        
        if self.bounds is not None:
            self.ax.set_extent([self.bounds.lon_min, self.bounds.lon_max,
                                self.bounds.lat_min, self.bounds.lat_max])  # Set map extent
        
        divider = make_axes_locatable(self.ax)  # Create a divider for colorbars
        return color, cmap, divider

    def add_coasts(self):
        """
        Adds coastlines to the map.
        """
        self.ax.coastlines()

    def add_bathy(self, show_bathy, divider):
        """
        Adds bathymetric data to the map as a filled contour plot, and creates a colorbar for it.
        
        Parameters:
        - show_bathy (bool): Whether to display bathymetric data.
        - divider (AxesDivider): Divider object for placing the bathymetry colorbar.
        """
        if show_bathy:
            bathy_contourf = self.ax.contourf(self.bathy.lon, self.bathy.lat, self.bathy.depth,
                                              levels=self.bathy.contour_levels, cmap=self.bathy.cmap,
                                              vmin=self.bathy.vmin, transform=ccrs.PlateCarree(), extend='both')
            # Add a colorbar for the bathymetry
            self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf, divider=divider,
                                                      fig=self.fig, nrows=self.nrows)

    def scatter(self, var: str | None = None, show_bathy: bool = True, pointsize=3, linewidths=0, grid=True, fig=None, ax=None) -> None:
        """
        Plots a scatter plot of points on the map, optionally including bathymetry and gridlines.
        
        Parameters:
        - var (str | None): The name of the variable to plot as color (e.g., temperature).
        - show_bathy (bool): Whether to show bathymetric data.
        - pointsize (int): Size of scatter plot points (default is 3).
        - linewidths (int): Line width of scatter plot points (default is 0).
        - grid (bool): Whether to display gridlines on the map (default is True).
        - fig (Figure): Matplotlib figure object (optional).
        - ax (Axes): Matplotlib axes object (optional).
        """
        color, cmap, divider = self.set_up_map(fig, ax, var)

        # Add bathymetry if needed
        self.add_bathy(show_bathy, divider)
        
        # Plot scatter points on the map
        self.sc = self.ax.scatter(self.instrument['lon'].data, self.instrument['lat'].data, linewidths=linewidths,
                                  c=color, cmap=cmap, s=pointsize, transform=ccrs.PlateCarree())
        # Add a colorbar for the scatter plot variable
        self.cbar_var = self.add_colorbar(self.sc, var, divider, total_cbars=(2 if show_bathy else 1))

        self.add_coasts()  # Add coastlines
        
        # Add gridlines if requested
        if grid:
            self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='gray',
                                        alpha=0.4, linestyle='--')
            self.gl.top_labels = False  # Disable top labels
            self.gl.right_labels = False  # Disable right labels
            self.gl.xformatter = LONGITUDE_FORMATTER  # Format x-axis as longitude
            self.gl.yformatter = LATITUDE_FORMATTER  # Format y-axis as latitude
            self.gl.xlocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for x-axis
            self.gl.ylocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for y-axis

    def quiver(self) -> None:
        """
        Placeholder for a method to plot vector fields on the map (e.g., currents).
        This method needs to be implemented.
        """
        raise NotImplementedError('Need to add Quiver')
