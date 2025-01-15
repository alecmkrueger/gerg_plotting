import unittest
import numpy as np
from unittest.mock import MagicMock
import cmocean
from datetime import datetime
import pytest

from gerg_plotting.data_classes.data import Data
from gerg_plotting.data_classes.variable import Variable
from gerg_plotting.data_classes.bounds import Bounds

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
        
    def test_init_variable_nonexistent(self):
        with self.assertRaises(ValueError):
            self.data._init_variable('nonexistent_var',cmap=cmocean.cm.thermal,units='K',vmin=0,vmax=200)
        
    def test_copy(self):
        """Test the copy method."""
        copied_data = self.data.copy()
        np.testing.assert_equal(self.data.lat.data, copied_data.lat.data)
        np.testing.assert_equal(self.data.lon.data, copied_data.lon.data)
        np.testing.assert_equal(self.data.depth.data, copied_data.depth.data)
        np.testing.assert_equal(self.data.time.data, copied_data.time.data)

    def test_calculate_speed(self):
        """Test speed calculation with and without w component."""
        self.data.u = Variable(data=np.array([3.0, 4.0]), name='u')
        self.data.v = Variable(data=np.array([4.0, 3.0]), name='v')
        self.data.calculate_speed(include_w=False)
        np.testing.assert_array_almost_equal(self.data.speed.data, np.array([5.0, 5.0]))
        
    def test_calculate_speed_include_w(self):
        """Test speed calculation with w component."""
        self.data.u = Variable(data=np.array([3.0, 4.0]), name='u')
        self.data.v = Variable(data=np.array([4.0, 3.0]), name='v')
        self.data.w = Variable(data=np.array([1.0, 1.0]), name='w')
        self.data.calculate_speed(include_w=True)
        np.testing.assert_array_almost_equal(self.data.speed.data, np.array([5.0, 5.0]))
        
    def test_psd_with_w(self):
        """Test PSD calculation with w component."""
        self.data.u = Variable(data=np.array([3.0, 4.0]), name='u')
        self.data.v = Variable(data=np.array([4.0, 3.0]), name='v')
        self.data.w = Variable(data=np.array([1.0, 1.0]), name='w')
        freq, psd_u, psd_v, psd_w = self.data.calcluate_PSD(sampling_freq=1.0, segment_length=1)
        self.assertIsInstance(freq, np.ndarray)

    def test_add_custom_variable(self):
        """Test adding custom variables."""
        new_var = Variable(data=np.array([1.0, 2.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        self.assertIn('custom_var', self.data.custom_variables)
        self.assertEqual(self.data.custom_var, new_var)
        
    def test_add_custom_variable_invaild_type(self):
        """Test adding custom variables."""
        with pytest.raises(TypeError,match='The provided object is not an instance of the Variable class.'):
            self.data.add_custom_variable('invalid_type')
            
    def test_add_custom_variable_already_exists(self):
        """Test adding custom variables."""
        new_var = Variable(data=np.array([1.0, 2.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        with pytest.raises(AttributeError,match="The variable 'custom_var' already exists."):
            self.data.add_custom_variable(new_var)

    def test_remove_custom_variable(self):
        """Test removing custom variables."""
        new_var = Variable(data=np.array([1.0, 2.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        self.data.remove_custom_variable('custom_var')
        self.assertNotIn('custom_var', self.data.custom_variables)
        
    def test_remove_invalid_custom_variable(self):
        """Test removing custom variables."""
        with self.assertRaises(KeyError):
            self.data.remove_custom_variable('lat')

    def test_slice_var(self):
        """Test variable slicing."""
        result = self.data.slice_var('lat', slice(0, 2))
        np.testing.assert_array_equal(result, self.test_data[0:2])

    def test_check_for_vars(self):
        """Test variable existence checking."""
        self.assertTrue(self.data.check_for_vars(['lat', 'lon']))
        with self.assertRaises(KeyError):
            self.data.check_for_vars(['nonexistent_var'])
    
    def test_check_for_vars_nonexistent_var(self):
        """Test variable existence checking for non-existent variables."""
        with self.assertRaises(KeyError):
            self.data.check_for_vars(['lat', 'nonexistent_var'])

    def test_check_for_vars_empty_list(self):
        """Test variable existence checking with an empty list."""
        with self.assertRaises(ValueError):
            self.data.check_for_vars([])

    def test_check_for_vars_missing_vars(self):
        """Test variable existence checking with missing variables."""
        with self.assertRaises(ValueError):
            self.data.check_for_vars(['w'])

    def test_date2num(self):
        """Test datetime conversion to numerical values."""
        result = self.data.date2num()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
    def test_date2num_not_time_present(self):
        """Test datetime conversion to numerical values when time is not present."""
        self.data.time = None
        with self.assertRaises(ValueError):
            self.data.date2num()

    def test_detect_bounds(self):
        """Test bounds detection."""
        bounds = self.data.detect_bounds(bounds_padding=0.1)
        self.assertIsInstance(bounds, Bounds)
        self.assertIsNotNone(bounds.lat_min)
        self.assertIsNotNone(bounds.lat_max)

    def test_detect_bounds_no_lat(self):
        """Test bounds detection when latitude is not present."""
        self.data.lat = None
        self.data.detect_bounds()
        self.assertIsNone(self.data.bounds.lat_min)
        self.assertIsNone(self.data.bounds.lat_max)

    def test_detect_bounds_no_lon(self):
        """Test bounds detection when latitude is not present."""
        self.data.lon = None
        self.data.detect_bounds()
        self.assertIsNone(self.data.bounds.lon_min)
        self.assertIsNone(self.data.bounds.lon_max)

    def test_detect_bounds_no_depth(self):
        """Test bounds detection when latitude is not present."""
        self.data.depth = None
        self.data.detect_bounds()
        self.assertIsNone(self.data.bounds.depth_top)
        self.assertIsNone(self.data.bounds.depth_bottom )

    def test_getitem(self):
        """Test variable access via indexing."""
        self.assertIsInstance(self.data['lat'], Variable)
        with self.assertRaises(KeyError):
            _ = self.data['nonexistent']
    
    def test_getitem_slice(self):
        """Test variable slicing via indexing."""
        result = self.data[0:2]
        np.testing.assert_array_equal(result.lat.data, self.test_data[0:2])

    def test_getitem_list(self):
        """Test variable slicing via indexing."""
        result = self.data[[0, 1]]
        np.testing.assert_array_equal(result.lat.data, self.test_data[0:2])
        np.testing.assert_array_equal(result.lon.data, self.test_data[0:2])

    def test_setitem(self):
        """Test variable assignment via indexing."""
        new_var = Variable(data=np.array([4.0, 5.0]), name='lat')
        self.data['lat'] = new_var
        np.testing.assert_array_equal(self.data.lat.data, new_var.data)
        
    def test_setitem_custom_varible(self):
        """Test variable assignment via indexing."""
        new_var = Variable(data=np.array([4.0, 5.0]), name='custom_var')
        self.data.add_custom_variable(new_var)
        new_var.data = np.array([5.0, 6.0])
        self.data['custom_var'] = new_var
        # with self.assertRaises():
        np.testing.assert_array_equal(self.data.custom_var.data, new_var.data)
    
    def test_setitem_invalid_var(self):
        """Test variable assignment via indexing."""
        new_var = Variable(data=np.array([4.0, 5.0]), name='lat')
        with self.assertRaises(KeyError):
            self.data['nonexistent'] = new_var
                
    def test_get_vars_all(self):
        """Test getting all variables regardless of data status."""
        vars_list = self.data.get_vars()
        expected_vars = ['lat', 'lon', 'depth', 'time', 'temperature', 'salinity', 
                        'density', 'u', 'v', 'w', 'speed', 'cdom', 'chlor', 'turbidity', 'bounds']
        self.assertEqual(set(vars_list), set(expected_vars))

    def test_get_vars_with_data(self):
        """Test getting only variables that have data."""
        vars_with_data = self.data.get_vars(have_data=True)
        expected_vars = ['lat', 'lon', 'depth', 'time']  # Based on setUp data
        self.assertEqual(set(vars_with_data), set(expected_vars))

    def test_get_vars_without_data(self):
        """Test getting only variables that don't have data."""
        vars_without_data = self.data.get_vars(have_data=False)
        expected_vars = ['temperature', 'salinity', 'density', 'u', 'v', 
                        'w', 'speed', 'cdom', 'chlor', 'turbidity', 'bounds']
        self.assertEqual(set(vars_without_data), set(expected_vars))

    def test_repr_html(self):
        """Test HTML representation of the Data object."""
        html_output = self.data._repr_html_()
        
        # Test that the HTML output is a string
        self.assertIsInstance(html_output, str)
        
        # Test that the HTML contains essential structural elements
        self.assertIn('<table', html_output)
        self.assertIn('</table>', html_output)
        self.assertIn('<thead>', html_output.lower())
        self.assertIn('<tbody>', html_output.lower())
        
        # Test that all variables with data are included in the HTML
        vars_with_data = self.data.get_vars(have_data=True)
        for var in vars_with_data:
            self.assertIn(var, html_output)


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
