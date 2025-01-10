import unittest
import numpy as np
from matplotlib.colors import Colormap
from unittest.mock import MagicMock

from gerg_plotting.data_classes.Bathy import Bathy
from gerg_plotting.data_classes.Bounds import Bounds

class TestBathy(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.bounds = Bounds(
            lat_min=25,
            lat_max=30,
            lon_min=-95,
            lon_max=-90,
            depth_bottom=1000,
            depth_top=0
        )
        self.bathy = Bathy(bounds=self.bounds)

    def test_initialization(self):
        """Test initialization and default attributes."""
        self.assertEqual(self.bathy.resolution_level, 5)
        self.assertEqual(self.bathy.contour_levels, 50)
        self.assertEqual(self.bathy.land_color, [231/255, 194/255, 139/255, 1])
        self.assertEqual(self.bathy.vmin, 0)
        self.assertIsInstance(self.bathy.cmap, Colormap)
        self.assertTrue(self.bathy.cbar_show)
        self.assertEqual(self.bathy.cbar_nbins, 5)

    def test_get_label(self):
        """Test label generation with and without vertical units."""
        self.assertEqual(self.bathy.get_label(), "Bathymetry (m)")
        self.bounds.vertical_units = "km"
        self.assertEqual(self.bathy.get_label(), "Bathymetry (km)")

    def test_init_without_bounds(self):
        """Test that class init raises error when bounds not set."""
        with self.assertRaises(ValueError):
            Bathy(bounds=None)

    def test_slice_var(self):
        """Test variable slicing functionality."""
        test_slice = slice(0, 5)
        self.bathy.depth = np.array([1, 2, 3, 4, 5, 6])
        result = self.bathy.slice_var('depth', test_slice)
        np.testing.assert_array_equal(result, np.array([1, 2, 3, 4, 5]))

    def test_has_var(self):
        """Test variable existence checking."""
        self.assertTrue(self.bathy._has_var('depth'))
        self.assertFalse(self.bathy._has_var('nonexistent_var'))

    def test_get_vars(self):
        """Test getting list of available variables."""
        vars_list = self.bathy.get_vars()
        self.assertIn('lat', vars_list)
        self.assertIn('lon', vars_list)
        self.assertIn('depth', vars_list)

    def test_copy(self):
        """Test deep copy functionality."""
        bathy_copy = self.bathy.copy()
        self.assertIsNot(bathy_copy, self.bathy)
        self.assertEqual(bathy_copy.resolution_level, self.bathy.resolution_level)

    def test_add_colorbar(self):
        """Test colorbar addition."""
        fig_mock = MagicMock()
        divider_mock = MagicMock()
        mappable_mock = MagicMock()
        self.bathy.add_colorbar(fig_mock, divider_mock, mappable_mock, nrows=1)
        self.assertIsNotNone(self.bathy.cbar)
