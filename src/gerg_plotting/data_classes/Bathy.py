import matplotlib.figure
import numpy as np
from attrs import define,field
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.colorbar
from matplotlib.colors import Colormap
import xarray as xr
from pathlib import Path
import cmocean

from gerg_plotting.modules.calculations import get_center_of_mass
from gerg_plotting.modules.plotting import colorbar
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.Bounds import Bounds

@define(repr=False)
class Bathy(SpatialInstrument):
    """
    Bathy class for handling bathymetry data and visualization.

    Attributes
    ----------
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
        # Load bathymetry data based on bounds
        self.get_bathy()
        # Scale depth values if a vertical scaler is provided
        if self.bounds.vertical_scaler is not None:
            self.depth = self.depth * self.bounds.vertical_scaler
        # Compute the center of mass of the bathymetry data
        self.center_of_mass = get_center_of_mass(self.lon, self.lat, self.depth)
        # Adjust the colormap for visualization
        self.adjust_cmap()

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
