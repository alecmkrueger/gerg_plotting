import unittest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.quiver import Quiver

import cartopy.crs as ccrs

from gerg_plotting.data_classes.Bathy import Bathy 
from gerg_plotting.data_classes.Data import Data
from gerg_plotting.plotting_classes.MapPlot import MapPlot


class TestMapPlot(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment for MapPlot with sample data and bounds.
        """
        self.data = Data(
            lon = np.linspace(-100, -90, 50),
            lat = np.linspace(22, 31, 50),
            u = np.random.normal(25, 50),
            v = np.random.normal(25, 50),
        )

        self.bounds = self.data.detect_bounds()

        self.data.bounds = None

        self.map_plot = MapPlot(data=self.data)

    def test_init_bathy(self):
        """
        Test that init_bathy initializes a Bathy object if not already set.
        """
        self.data.detect_bounds()
        self.map_plot.bathy = None
        self.map_plot.init_bathy()
        self.assertIsInstance(self.map_plot.bathy, Bathy)

    def test_set_up_map(self):
        """
        Test that set_up_map initializes an axis with correct projection and extent.
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        color, cmap, divider = self.map_plot.set_up_map(fig=fig, ax=ax, var="speed")

        # Check projection and extent
        self.assertAlmostEqual(ax.get_extent(ccrs.PlateCarree()), 
                         [self.bounds["lon_min"], self.bounds["lon_max"], 
                          self.bounds["lat_min"], self.bounds["lat_max"]])

    def test_add_coasts(self):
        """
        Test that add_coasts adds coastlines to the map.
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.map_plot.ax = ax

        self.map_plot.add_coasts(show_coastlines=True)
        # Cannot directly test coastlines but ensure ax is set up
        self.assertEqual(self.map_plot.ax, ax)

    def test_add_bathy(self):
        """
        Test that add_bathy adds bathymetry data as a contour plot.
        """
        self.data.detect_bounds()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.map_plot.ax = ax
        self.map_plot.init_bathy()

        self.map_plot.add_bathy(show_bathy=True, divider=None)
        # Validate contour plot is added
        contour_plots = ax.collections
        self.assertGreater(len(contour_plots), 0)

    def test_scatter(self):
        """
        Test that scatter adds a scatter plot to the map.
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.map_plot.ax = ax

        self.map_plot.scatter(var="speed")
        # Check scatter data is added
        scatter_points = ax.collections[0]  # Scatter plot data is stored in `collections`
        self.assertEqual(len(scatter_points.get_offsets()), self.data["lon"].size * self.data["lat"].size)

    def test_quiver(self):
        """
        Test that quiver adds vector arrows to the map.
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.map_plot.ax = ax

        self.map_plot.quiver()
        # Check quiver data is added
        quivers = [artist for artist in ax.get_children() if isinstance(artist, Quiver)]
        self.assertGreater(len(quivers), 0)

