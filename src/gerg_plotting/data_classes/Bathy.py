import matplotlib.figure
import numpy as np
from attrs import define,field,asdict
from pprint import pformat
from typing import Iterable
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.colorbar
from matplotlib.colors import Colormap
import matplotlib.dates as mdates
import xarray as xr
from pathlib import Path
import cmocean
import copy


from gerg_plotting.modules.calculations import get_center_of_mass
from gerg_plotting.modules.plotting import colorbar
from gerg_plotting.modules.utilities import calculate_pad

from gerg_plotting.data_classes.Bounds import Bounds
from gerg_plotting.data_classes.Variable import Variable

@define(repr=False)
class Bathy:
    """
    Bathy class for handling bathymetry data and visualization.

    Attributes
    ----------
    lat : Iterable | Variable | None
        Latitude values or Variable object containing latitude data
    lon : Iterable | Variable | None
        Longitude values or Variable object containing longitude data
    depth : Iterable | Variable | None
        Depth values or Variable object containing depth data
    time : Iterable | Variable | None
        Time values or Variable object containing temporal data
    bounds : Bounds, optional
        Geographic and depth bounds for the dataset
    custom_variables : dict
        Dictionary to store additional custom variables
    bounds : Bounds
        Object containing spatial and vertical boundaries for the dataset.
    resolution_level : float or int, optional
        Degree resolution for coarsening the dataset, default is 5.
    contour_levels : int, optional
        Number of contour levels for visualization, default is 50.
    land_color : list
        RGBA color values for representing land, default is [231/255, 194/255, 139/255, 1].
    vmin : float or int, optional
        Minimum value for the colormap, default is 0.
    cmap : Colormap
        Colormap for bathymetry visualization, default is 'Blues'.
    cbar_show : bool
        Whether to display a colorbar, default is True.
    cbar : matplotlib.colorbar.Colorbar
        Colorbar for the bathymetry visualization.
    cbar_nbins : int
        Number of bins for colorbar ticks, default is 5.
    cbar_kwargs : dict
        Additional keyword arguments for the colorbar.
    center_of_mass : tuple
        Center of mass of the bathymetry data (longitude, latitude, depth).
    label : str
        Label for the bathymetry data, default is 'Bathymetry'.
    """
    # Dims
    lat: Iterable|Variable|None = field(default=None)
    lon: Iterable|Variable|None = field(default=None)
    depth: Iterable|Variable|None = field(default=None)
    time: Iterable|Variable|None = field(default=None)
    
    bounds: Bounds = field(default=None)
    resolution_level: float | int | None = field(default=5)
    contour_levels: int = field(default=50)
    land_color: list = field(default=[231 / 255, 194 / 255, 139 / 255, 1])
    vmin: int | float = field(default=0)
    cmap: Colormap = field(default=matplotlib.colormaps.get_cmap('Blues'))
    cbar_show: bool = field(default=True)
    cbar: matplotlib.colorbar.Colorbar = field(init=False)
    cbar_nbins: int = field(default=5)
    cbar_kwargs: dict = field(default={})
    center_of_mass: tuple = field(init=False)
    label: str = field(default='Bathymetry')

    def __attrs_post_init__(self) -> None:
        """
        Post-initialization method to process bathymetry data and adjust colormap.
        """
        self._init_dims()
        self._format_datetime()
        # Load bathymetry data based on bounds
        self.get_bathy()
        # Scale depth values if a vertical scaler is provided
        if self.bounds.vertical_scaler is not None:
            self.depth = self.depth * self.bounds.vertical_scaler
        # Compute the center of mass of the bathymetry data
        self.center_of_mass = get_center_of_mass(self.lon, self.lat, self.depth)
        # Adjust the colormap for visualization
        self.adjust_cmap()
        

    def copy(self):
        """Creates a deep copy of the instrument object."""
        self_copy = copy.deepcopy(self)
        return self_copy
    

    def slice_var(self,var:str,slice:slice) -> np.ndarray:
        """Slices data for a specific variable."""
        return self[var].data[slice]


    def _has_var(self, key) -> bool:
        """Checks if a variable exists in the instrument."""
        return key in asdict(self).keys() or key in self.custom_variables
    

    def get_vars(self) -> list:
        """Gets a list of all available variables."""
        vars = list(asdict(self).keys()) + list(self.custom_variables.keys())
        vars = [var for var in vars if var!='custom_variables']
        return vars


    def __getitem__(self, key) -> Variable:
        """Allows accessing standard and custom variables via indexing."""
        if isinstance(key,slice):
            self_copy = self.copy()
            for var_name in self.get_vars():
                if isinstance(self_copy[var_name],Variable):
                    self_copy[var_name].data = self.slice_var(var=var_name,slice=key)
            return self_copy
        elif self._has_var(key):
            return getattr(self, key, self.custom_variables.get(key))
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")    


    def __setitem__(self, key, value) -> None:
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            if key in asdict(self):
                setattr(self, key, value)
            else:
                self.custom_variables[key] = value
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")


    def __repr__(self) -> None:
        '''Pretty printing'''
        return pformat(asdict(self),width=1)
    

    def _init_dims(self):
        """Initialize standard dimensions (lat, lon, depth, time) as Variable objects."""
        self._init_variable(var='lat', cmap=cmocean.cm.haline, units='°N', vmin=None, vmax=None)
        self._init_variable(var='lon', cmap=cmocean.cm.thermal, units='°E', vmin=None, vmax=None)
        self._init_variable(var='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
        self._init_variable(var='time', cmap=cmocean.cm.thermal, units=None, vmin=None, vmax=None)

    def _format_datetime(self) -> None:
        """Format datetime data as numpy datetime64 objects."""
        if self.time is not None:
            if self.time.data is not None:
                self.time.data = self.time.data.astype('datetime64[ns]')

    def _init_variable(self, var: str, cmap, units, vmin, vmax) -> None:
        """
        Initialize a standard variable as a Variable object.

        Parameters
        ----------
        var : str
            Name of the variable to initialize
        cmap : matplotlib.colors.Colormap
            Colormap for variable visualization
        units : str
            Units of the variable
        vmin : float | None
            Minimum value for visualization
        vmax : float | None
            Maximum value for visualization
        """        
        if self._has_var(var):
            if not isinstance(self[var],Variable):
                if self[var] is not None:    
                    self[var] = Variable(
                        data=self[var],
                        name=var,
                        cmap=cmap,
                        units=units,
                        vmin=vmin,
                        vmax=vmax
                    )
        else:
            raise ValueError(f'{var} does not exist, try using the add_custom_variable method')
        


    def check_for_vars(self,vars:list) -> bool:
        """
        Verify that all required variables exist in the dataset.

        Parameters
        ----------
        vars : list
            List of variable names to check

        Returns
        -------
        bool
            True if all variables exist

        Raises
        ------
        ValueError
            If any required variables are missing
        """
        vars = [var for var in vars if var is not None]
        vars = [var for var in vars if self[var] is None]
        if vars:
            raise ValueError(
                f"The following required variables are missing: {', '.join(vars)}. "
                "Please ensure the Data object includes data for all listed variables."
            )
        return True


    def date2num(self) -> list:
        """Converts time data to numerical values."""
        if self.time is not None:
            if self.time.data is not None:
                return list(mdates.date2num(self.time.data))
        else: raise ValueError('time variable not present')


    def detect_bounds(self,bounds_padding=0) -> Bounds:
        '''
        Detect the geographic bounds of the data, applying padding if specified.

        An intentional effect of this function:
            will only calculate the bounds when self.bounds is None,
            so that it does not overwrite the user's custom bounds,
            this will also ensure that the bounds is not repeatedly calculated unless desired,
            can recalculate self.bounds using a new bounds_padding value if self.bounds is set to None

        The depth bounds are not affected by the bounds padding, therfore the max and min values of the depth data are used

        Parameters
        ----------
        bounds_padding : float, optional
            Padding to add to the detected bounds, by default 0

        Returns
        -------
        Bounds
            Object containing the detected geographic and depth bounds
        """

        '''
        # If the user did not pass bounds
        if self.bounds is None:
            # Detect and calculate the lat bounds with padding
            if self.lat is not None:
                lat_min, lat_max = calculate_pad(self.lat.data, pad=bounds_padding)
            else:
                lat_min, lat_max = None, None
            # Detect and calculate the lon bounds with padding
            if self.lon is not None:
                lon_min, lon_max = calculate_pad(self.lon.data, pad=bounds_padding)
            else:
                lon_min, lon_max = None, None
            
            # depth_bottom: positive depth example: 1000
            # depth_top:positive depth example for surface: 0
            
            if self.depth is not None:
                depth_top, depth_bottom = calculate_pad(self.depth.data)
            else:
                depth_top, depth_bottom = None,None
                
            # Set the bounds
            self.bounds = Bounds(
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                depth_bottom=depth_bottom,
                depth_top=depth_top
            )

        return self.bounds

    def get_label(self) -> str:
        """
        Get the label for the bathymetry data, including units if provided.

        Returns
        -------
        str
            Label for the bathymetry data.
        """
        # Update label with vertical units if they exist
        if self.bounds.vertical_units != '':
            self.label = f"Bathymetry ({self.bounds.vertical_units})"
        return self.label

    def adjust_cmap(self) -> None:
        """
        Adjust the colormap by cropping and adding land color.
        """
        # Crop the lower 20% of the colormap
        self.cmap = cmocean.tools.crop_by_percent(self.cmap, 20, 'min')
        # Set the under color (land color) for the colormap
        self.cmap.set_under(self.land_color)

    def get_bathy(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load and process bathymetry data.

        Returns
        -------
        tuple of np.ndarray
            Longitude, latitude, and depth values.

        Raises
        ------
        ValueError
            If the bounds attribute is not provided.
        """
        if self.bounds is None:
            raise ValueError(f'The map bounds are not found')

        # Define the path to the seafloor data file
        self_path = Path(__file__).parent
        seafloor_path = self_path.parent.joinpath('seafloor_data/seafloor_data.nc')
        ds = xr.open_dataset(seafloor_path)  # Read in seafloor data

        # Slice the dataset to match the spatial bounds
        ds = ds.sel(lat=slice(self.bounds["lat_min"], self.bounds["lat_max"])).sel(
            lon=slice(self.bounds["lon_min"], self.bounds["lon_max"])
        )

        # Coarsen the dataset to improve performance, if resolution_level is set
        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level, boundary='trim').mean().coarsen(
                lon=self.resolution_level, boundary='trim'
            ).mean()  # type: ignore

        # Extract and flip depth values
        self.depth = ds['elevation'].values * -1

        # Apply depth constraints for visualization
        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth > self.bounds["depth_top"], self.depth, self.bounds["depth_top"])
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth < self.bounds["depth_bottom"], self.depth, self.bounds["depth_bottom"])

        # Extract latitude and longitude values
        self.lon = ds.coords['lat'].values
        self.lat = ds.coords['lon'].values
        # Create a meshgrid for plotting
        self.lon, self.lat = np.meshgrid(self.lat, self.lon)

        return self.lon, self.lat, self.depth

    def add_colorbar(self, fig: matplotlib.figure.Figure, divider, mappable: matplotlib.axes.Axes, nrows: int) -> None:
        """
        Add a colorbar to the figure.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The figure to which the colorbar is added.
        divider : AxesDivider
            Divider to place the colorbar appropriately.
        mappable : matplotlib.axes.Axes
            The mappable object (e.g., image or contour plot).
        nrows : int
            Number of rows in the figure layout.

        Returns
        -------
        matplotlib.colorbar.Colorbar
            The created colorbar instance.
        """
        if self.cbar_show:
            # Get the label for the colorbar
            label = self.get_label()
            # Create the colorbar using custom parameters
            self.cbar = colorbar(fig, divider, mappable, label, nrows=nrows)
            # Adjust colorbar ticks and invert the y-axis
            self.cbar.ax.locator_params(nbins=self.cbar_nbins)
            self.cbar.ax.invert_yaxis()
            return self.cbar
