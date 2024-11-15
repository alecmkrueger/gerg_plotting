from gerg_plotting.modules.validations import lat_min_smaller_than_max,lon_min_smaller_than_max,is_flat_numpy_array

import unittest
import numpy as np
from unittest.mock import MagicMock


class TestLatMinSmallerThanMax(unittest.TestCase):
    def test_valid_lat_min(self):
        """Test that no error is raised for valid lat_min."""
        mock_instance = MagicMock(lat_max=10)
        lat_min_smaller_than_max(mock_instance, None, 5)  # Should not raise

    def test_invalid_lat_min(self):
        """Test that ValueError is raised when lat_min >= lat_max."""
        mock_instance = MagicMock(lat_max=10)
        with self.assertRaises(ValueError):
            lat_min_smaller_than_max(mock_instance, None, 15)


class TestLonMinSmallerThanMax(unittest.TestCase):
    def test_valid_lon_min(self):
        """Test that no error is raised for valid lon_min."""
        mock_instance = MagicMock(lon_max=20)
        lon_min_smaller_than_max(mock_instance, None, 10)  # Should not raise

    def test_invalid_lon_min(self):
        """Test that ValueError is raised when lon_min >= lon_max."""
        mock_instance = MagicMock(lon_max=20)
        with self.assertRaises(ValueError):
            lon_min_smaller_than_max(mock_instance, None, 25)


class TestIsFlatNumpyArray(unittest.TestCase):
    def test_valid_flat_array(self):
        """Test that no error is raised for valid flat NumPy array."""
        mock_attribute = MagicMock(name="attribute_name")
        is_flat_numpy_array(None, mock_attribute, np.array([1, 2, 3]))  # Should not raise

    def test_invalid_type(self):
        """Test that ValueError is raised when input is not a NumPy array."""
        mock_attribute = MagicMock(name="attribute_name")
        with self.assertRaises(ValueError):
            is_flat_numpy_array(None, mock_attribute, [1, 2, 3])  # List is invalid

    def test_invalid_shape(self):
        """Test that ValueError is raised for non-flat arrays."""
        mock_attribute = MagicMock(name="attribute_name")
        with self.assertRaises(ValueError):
            is_flat_numpy_array(None, mock_attribute, np.array([[1, 2], [3, 4]]))