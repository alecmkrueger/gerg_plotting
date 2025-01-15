from gerg_plotting.data_classes.bounds import Bounds

import unittest


class TestBounds(unittest.TestCase):
    def setUp(self):
        """Set up a Bounds instance with default parameters for testing."""
        self.bounds = Bounds(
            lat_min=10,
            lat_max=20,
            lon_min=30,
            lon_max=40,
            depth_bottom=1000,
            depth_top=0,
        )

    def test_initialization(self):
        """Test initialization with valid values."""
        self.assertEqual(self.bounds.lat_min, 10)
        self.assertEqual(self.bounds.lat_max, 20)
        self.assertEqual(self.bounds.lon_min, 30)
        self.assertEqual(self.bounds.lon_max, 40)
        self.assertEqual(self.bounds.depth_bottom, 1000)
        self.assertEqual(self.bounds.depth_top, 0)

    def test_invalid_lat_min(self):
        """Test lat_min validation."""
        with self.assertRaises(TypeError):
            Bounds(lat_min="invalid", lat_max=20)

    def test_invalid_lon_min(self):
        """Test lon_min validation."""
        with self.assertRaises(TypeError):
            Bounds(lon_min="invalid", lon_max=40)

    def test_lat_min_smaller_than_lat_max(self):
        """Test lat_min < lat_max validation."""
        with self.assertRaises(ValueError):
            Bounds(lat_min=30, lat_max=20)

    def test_lon_min_smaller_than_lon_max(self):
        """Test lon_min < lon_max validation."""
        with self.assertRaises(ValueError):
            Bounds(lon_min=50, lon_max=40)

    def test_dict_style_access_get(self):
        """Test __getitem__ for accessing attributes."""
        self.assertEqual(self.bounds["lat_min"], 10)
        self.assertEqual(self.bounds["lon_max"], 40)

        with self.assertRaises(KeyError):
            _ = self.bounds["invalid_key"]

    def test_dict_style_access_set(self):
        """Test __setitem__ for modifying attributes."""
        self.bounds["lat_min"] = 15
        self.assertEqual(self.bounds.lat_min, 15)

        with self.assertRaises(KeyError):
            self.bounds["invalid_key"] = 50

    def test_repr(self):
        """Test __repr__ for pretty-printing."""
        expected_repr = (
            "{'depth_bottom': 1000,\n"
            " 'depth_top': 0,\n"
            " 'lat_max': 20,\n"
            " 'lat_min': 10,\n"
            " 'lon_max': 40,\n"
            " 'lon_min': 30,\n"
            " 'vertical_scaler': 1,\n"
            " 'vertical_units': 'm'}"
        )
        self.assertEqual(repr(self.bounds), expected_repr,f'{repr(self.bounds)}')
