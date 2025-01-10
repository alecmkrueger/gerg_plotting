import unittest
import numpy as np
from unittest.mock import MagicMock
import cmocean
from datetime import datetime

from gerg_plotting.data_classes.Data import Data
from gerg_plotting.data_classes.Variable import Variable
from gerg_plotting.data_classes.Bounds import Bounds

class TestData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_data = np.array([1.0, 2.0, 3.0])
        self.data = Data(
            lat=self.test_data,
            lon=self.test_data,
            depth=self.test_data,
            time=np.array([datetime(2023, 1, 1), datetime(2023, 1, 2)])
        )

    def test_initialization(self):
        """Test initialization and automatic Variable conversion."""
        self.assertIsInstance(self.data.lat, Variable)
        self.assertIsInstance(self.data.lon, Variable)
        self.assertIsInstance(self.data.depth, Variable)
        self.assertIsInstance(self.data.time, Variable)

    def test_calculate_speed(self):
        """Test speed calculation with and without w component."""
        self.data.u = Variable(data=np.array([3.0, 4.0]), name='u')
        self.data.v = Variable(data=np.array([4.0, 3.0]), name='v')
        self.data.calculate_speed(include_w=False)
        np.testing.assert_array_almost_equal(self.data.speed.data, np.array([5.0, 5.0]))

    def test_add_custom_variable(self):
        """Test adding custom variables."""
        new_var = Variable(data=np.array([1.0, 2.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        self.assertIn('custom_var', self.data.custom_variables)
        self.assertEqual(self.data.custom_var, new_var)

    def test_remove_custom_variable(self):
        """Test removing custom variables."""
        new_var = Variable(data=np.array([1.0, 2.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        self.data.remove_custom_variable('custom_var')
        self.assertNotIn('custom_var', self.data.custom_variables)

    def test_slice_var(self):
        """Test variable slicing."""
        result = self.data.slice_var('lat', slice(0, 2))
        np.testing.assert_array_equal(result, self.test_data[0:2])

    def test_check_for_vars(self):
        """Test variable existence checking."""
        self.assertTrue(self.data.check_for_vars(['lat', 'lon']))
        with self.assertRaises(KeyError):
            self.data.check_for_vars(['nonexistent_var'])

    def test_date2num(self):
        """Test datetime conversion to numerical values."""
        result = self.data.date2num()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_detect_bounds(self):
        """Test bounds detection."""
        bounds = self.data.detect_bounds(bounds_padding=0.1)
        self.assertIsInstance(bounds, Bounds)
        self.assertIsNotNone(bounds.lat_min)
        self.assertIsNotNone(bounds.lat_max)

    def test_getitem(self):
        """Test variable access via indexing."""
        self.assertIsInstance(self.data['lat'], Variable)
        with self.assertRaises(KeyError):
            _ = self.data['nonexistent']

    def test_setitem(self):
        """Test variable assignment via indexing."""
        new_var = Variable(data=np.array([4.0, 5.0]), name='lat')
        self.data['lat'] = new_var
        np.testing.assert_array_equal(self.data.lat.data, new_var.data)

    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.data)
        self.assertIsInstance(repr_str, str)
        self.assertIn('lat', repr_str)
        self.assertIn('lon', repr_str)

    def test_format_datetime(self):
        """Test datetime formatting."""
        formatted_time = self.data.time.data
        self.assertEqual(formatted_time.dtype.kind, 'M')
