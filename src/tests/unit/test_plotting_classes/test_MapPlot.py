import unittest
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
from gerg_plotting.data_classes.Bathy import Bathy
from gerg_plotting.data_classes.Data import Data
from gerg_plotting.plotting_classes.MapPlot import MapPlot


class TestMapPlot(unittest.TestCase):
    def setUp(self):
        # Set up dummy data and instances for testing
        self.data = {
            'lon': np.linspace(-100, -80, 100),
            'lat': np.linspace(20, 40, 100),
            'depth':np.linspace(0,200,100),
            'temperature': np.random.rand(100),
            'salinity': np.random.rand(100),
            'u': np.random.rand(100),
            'v': np.random.rand(100),
            'speed': np.random.rand(100),
        }
        self.data = Data(**self.data)
        self.data.detect_bounds()
        self.bathy = Bathy(bounds=self.data.bounds)
        self.map_plot = MapPlot(data=self.data, bathy=self.bathy)

    def test_init_bathy(self):
        """Test that the bathy object is initialized correctly."""
        self.map_plot.init_bathy()
        self.assertIsInstance(self.map_plot.bathy, Bathy)

    def test_set_up_map(self):
        """Test the map setup process and returned values."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        color, cmap, divider = self.map_plot.set_up_map(fig=fig, ax=ax, var='temperature')
        self.assertIsInstance(color, np.ndarray)
        self.assertIsNotNone(cmap)
        self.assertIsNotNone(divider)

    def test_add_coasts(self):
        """Test adding coastlines to the map."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        self.map_plot.init_figure(fig=fig, ax=ax, geography=True)
        self.map_plot.add_coasts(show_coastlines=True)
        # No exception indicates success; visual testing can verify coastlines.

    def test_add_grid(self):
        """Test adding gridlines to the map."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        self.map_plot.init_figure(fig=fig, ax=ax, geography=True)
        self.map_plot.add_grid(grid=True)
        self.assertIsNotNone(self.map_plot.gl)

    def test_add_bathy(self):
        """Test adding bathymetry data to the map."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        divider = plt.figure().add_axes([0, 0, 1, 1])
        divider = make_axes_locatable(divider)
        self.map_plot.init_figure(fig=fig, ax=ax, geography=True)
        self.map_plot.add_bathy(show_bathy=True, divider=divider)
        self.assertIsNotNone(self.map_plot.cbar_bathy)

    def test_scatter(self):
        """Test scatter plot functionality."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        self.map_plot.init_figure(fig=fig, ax=ax, geography=True)
        self.map_plot.scatter(var='temperature', fig=fig, ax=ax)
        self.assertIsNotNone(self.map_plot.sc)
        self.assertIsNotNone(self.map_plot.cbar_var)

    def test_quiver(self):
        """Test quiver plot functionality."""
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        self.map_plot.init_figure(fig=fig, ax=ax, geography=True)
        self.map_plot.quiver(fig=fig, ax=ax)
        self.assertIsNotNone(self.map_plot.cbar_var)


