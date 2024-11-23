from gerg_plotting.data_classes.Bathy import Bathy
from gerg_plotting.data_classes.Bounds import Bounds

import unittest
import numpy as np
from pathlib import Path
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from matplotlib.colorbar import Colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


class TestBathy(unittest.TestCase):
    def setUp(self):
        """Set up a Bathy instance with mocked data."""
        self.bounds = Bounds(
            lat_min=10,
            lon_min=20,
            lat_max=30,
            lon_max=40,
            depth_top=0,
            depth_bottom=5000,
        )
        self.bathy = Bathy(bounds=self.bounds)

    def test_initialization(self):
        """Test initialization and default attributes."""
        self.assertEqual(self.bathy.resolution_level, 5)
        self.assertEqual(self.bathy.contour_levels, 50)
        self.assertEqual(self.bathy.land_color, [231 / 255, 194 / 255, 139 / 255, 1])
        self.assertEqual(self.bathy.vmin, 0)
        self.assertIsInstance(self.bathy.cmap, Colormap)
        self.assertTrue(self.bathy.cbar_show)
        self.assertEqual(self.bathy.cbar_nbins, 5)
        self.assertEqual(self.bathy.label, "Bathymetry")

    def test_get_label(self):
        """Test that the label updates correctly with vertical units."""
        self.assertEqual(self.bathy.get_label(), "Bathymetry (m)")
        self.bathy.bounds.vertical_units = "km"
        self.assertEqual(self.bathy.get_label(), "Bathymetry (km)")

    def test_adjust_cmap(self):
        """Test that the colormap is adjusted correctly."""
        original_cmap = self.bathy.cmap
        self.bathy.adjust_cmap()
        self.assertNotEqual(self.bathy.cmap, original_cmap)  # Ensure colormap was modified

    def test_get_bathy(self):
        """Test the get_bathy method for proper depth, lon, and lat extraction."""
        # This test assumes the presence of the file defined in the get_bathy method.
        lon, lat, depth = self.bathy.get_bathy()
        self.assertIsInstance(lon, np.ndarray)
        self.assertIsInstance(lat, np.ndarray)
        self.assertIsInstance(depth, np.ndarray)
        self.assertEqual(lon.shape, lat.shape)  # lon and lat should have the same shape as meshgrid
        self.assertEqual(depth.shape, lon.shape)  # depth should align with lon/lat meshgrid

    def test_get_bathy_missing_bounds(self):
        """Test the get_bathy method for proper depth, lon, and lat extraction."""
        # This test assumes the presence of the file defined in the get_bathy method.
        self.bathy.bounds = None
        with self.assertRaises(ValueError):
            self.bathy.get_bathy()

    def test_add_colorbar(self):
        """Test the add_colorbar method."""
        fig, ax = plt.subplots()
        mock_divider = make_axes_locatable(ax)  # Create a divider for colorbars
        mock_mappable = None  # You can pass a mock or real mappable as per your test setup
        nrows = 1

        self.bathy.add_colorbar(fig, mock_divider, mock_mappable, nrows)
        self.assertIsInstance(self.bathy.cbar, Colorbar)
        self.assertEqual(self.bathy.cbar.locator._nbins,5)  # Check if nbins is working
        self.assertEqual(self.bathy.cbar.ax.get_ylabel(), "Bathymetry (m)")  # Check if the label is being assigned
        self.assertTrue(self.bathy.cbar.ax.yaxis_inverted())


    def test_vertical_scaler(self):
        """Test that the vertical_scaler adjusts the depth correctly."""
        initial_depth = self.bathy.depth.copy() if hasattr(self.bathy, 'depth') else None
        self.bathy.vertical_scaler = 2
        self.bathy.__attrs_post_init__()  # Reapply initialization logic
        if initial_depth is not None:
            np.testing.assert_array_equal(self.bathy.depth, initial_depth * 2)
