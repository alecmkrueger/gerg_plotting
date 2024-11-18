import unittest
from gerg_plotting.data_classes.Variable import Variable
from gerg_plotting.data_classes.Bounds import Bounds
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

class TestSpatialInstrument(unittest.TestCase):

    def setUp(self):
        # Set up some default values for testing
        self.variable_data = np.array([1, 2, 3, 4, 5])
        self.time_variable_data = pd.date_range(start='2024-08-13',end='2024-08-18')
        self.spatial_instrument = SpatialInstrument(lat=self.variable_data, lon=self.variable_data, depth=self.variable_data, time=self.time_variable_data)

    def test_initialization(self):
        """Test the initialization of SpatialInstrument with provided values."""
        self.assertEqual(self.spatial_instrument.lat.data.tolist(), self.variable_data.tolist())
        self.assertEqual(self.spatial_instrument.lon.data.tolist(), self.variable_data.tolist())
        self.assertEqual(self.spatial_instrument.depth.data.tolist(), self.variable_data.tolist())
        # For some reason numpy's built-in method .tolist() converts the datetime format to int instead of the expected str
        # so we need to use the list() constructor instead
        self.assertEqual(list(self.spatial_instrument.time.data), self.time_variable_data.tolist())

    def test_copy(self):
        """Test the copy method."""
        instrument_copy = self.spatial_instrument.copy()
        self.assertNotEqual(id(self.spatial_instrument), id(instrument_copy))  # Ensure it's a deep copy
        self.assertEqual(self.spatial_instrument.lat.data.tolist(), instrument_copy.lat.data.tolist())

    def test_get_vars(self):
        """Test the get_vars method."""
        expected_vars = ['lat', 'lon', 'depth', 'time']
        actual_vars = self.spatial_instrument.get_vars()
        self.assertTrue(all(var in actual_vars for var in expected_vars))

    def test_setitem_getitem(self):
        """Test __getitem__ and __setitem__ methods."""
        # Test setting and getting a standard variable
        self.spatial_instrument['lat'] = np.array([6, 7, 8, 9, 10])
        self.assertEqual(self.spatial_instrument['lat'].data.tolist(), [6, 7, 8, 9, 10])

        # Test getting a custom variable
        custom_var = Variable(data=np.array([11, 12, 13, 14, 15]), name="custom_var", cmap=None, units="units")
        self.spatial_instrument.add_custom_variable(custom_var)
        self.assertEqual(self.spatial_instrument['custom_var'].data.tolist(), [11, 12, 13, 14, 15])

        # Test setting a custom variable after adding a custom variable
        self.spatial_instrument['custom_var'] = [1,2,3,4]

        # Test getting a non-existing variable
        with self.assertRaises(KeyError):
            self.spatial_instrument['non_existing_var']


    def test_setitem_invalid(self):
        with self.assertRaises(KeyError):
            self.spatial_instrument['invalid_key'] = [1,2,3,4]

    def test_remove_custom_variable(self):
        """Test removing a custom variable."""
        custom_var = Variable(data=np.array([1, 2, 3]), name="remove_var", cmap=None, units="units")
        self.spatial_instrument.add_custom_variable(custom_var)
        self.assertTrue(hasattr(self.spatial_instrument, "remove_var"))
        self.spatial_instrument.remove_custom_variable("remove_var")
        self.assertFalse(hasattr(self.spatial_instrument, "remove_var"))

    def test_check_for_vars(self):
        """Test the check_for_vars method."""
        # Add a custom variable and check for it
        custom_var = Variable(data=np.array([10, 20, 30]), name="check_var", cmap=None, units="units")
        self.spatial_instrument.add_custom_variable(custom_var)
        self.assertTrue(self.spatial_instrument.check_for_vars(["check_var"]))

        # Check for missing variable (should raise an exception)
        # Remove the variable lat
        self.spatial_instrument['lat'] = None
        with self.assertRaises(ValueError):
            self.spatial_instrument.check_for_vars(["lat"])

    def test_detect_bounds(self):
        """Test the detect_bounds method."""
        bounds = self.spatial_instrument.detect_bounds()
        self.assertIsInstance(bounds, Bounds)

    def test_detect_bounds_if_given_by_user(self):
        # Test if bounds is given by the user
        bounds = Bounds(lat_min=None,lat_max=None,lon_min=None,lon_max=None,depth_bottom=None,depth_top=None)
        self.spatial_instrument.bounds = bounds
        bounds_detected = self.spatial_instrument.detect_bounds()
        self.assertEqual(bounds,bounds_detected)

    def test_detect_bounds_lat_lon_missing(self):
        # Test if lat and/or lon variables are missing
        self.spatial_instrument.lat = None
        self.spatial_instrument.lon = None
        self.spatial_instrument.detect_bounds()
        lat_min = self.spatial_instrument.bounds.lat_min
        lat_max = self.spatial_instrument.bounds.lat_max
        self.assertIsNone(lat_min)
        self.assertIsNone(lat_max)

    def test_detect_bounds_with_bounds_padding(self):
        bounds = self.spatial_instrument.detect_bounds(bounds_padding=1)

        self.assertEqual(self.spatial_instrument.bounds,bounds)

        # Check to ensure the depth is not affected by the bounds_padding parameter
        self.assertEqual(bounds.depth_top,1,f'{bounds}')
        self.assertEqual(bounds.depth_bottom,5)

        self.assertEqual(bounds.lat_min,0)
        self.assertEqual(bounds.lat_max,6)

        self.assertEqual(bounds.lon_min,0)
        self.assertEqual(bounds.lon_max,6)


    def test_format_datetime(self):
        """Test the _format_datetime method."""
        time_var = Variable(data=np.array(["2024-01-01", "2024-01-02", "2024-01-03"], dtype='datetime64[D]'),
                            name="time", cmap=None, units="units")
        self.spatial_instrument.time = time_var
        self.spatial_instrument._format_datetime()
        self.assertEqual(self.spatial_instrument.time.data[0], np.datetime64("2024-01-01"))

    def test_init_variable(self):
        """Test the _init_variable method."""
        self.spatial_instrument._init_variable('lat', cmap=None, units='°N', vmin=None, vmax=None)
        self.assertTrue(isinstance(self.spatial_instrument.lat, Variable))

        # Test for a non-existing variable to raise an error
        with self.assertRaises(ValueError):
            self.spatial_instrument._init_variable('non_existing_var', cmap=None, units=None, vmin=None, vmax=None)

    def test_slicing(self):
        """Test slicing functionality."""
        sliced_instrument = self.spatial_instrument[:3]
        self.assertEqual(sliced_instrument['lat'].data.tolist(), [1, 2, 3])

    def test_add_custom_variable(self):
        """Test adding a custom variable."""
        custom_var = Variable(data=np.array([100, 200, 300]), name="custom_var", cmap=None, units="units")
        self.spatial_instrument.add_custom_variable(custom_var)
        self.assertTrue(hasattr(self.spatial_instrument, "custom_var"))
        self.assertEqual(self.spatial_instrument.custom_var.data.tolist(), [100, 200, 300])

        # Test not passing a Variable object
        with self.assertRaises(TypeError):
            self.spatial_instrument.add_custom_variable([1,2,3,4])

        # Test if the variable already exists and exists_ok = False
        lat = Variable(data=np.array([100, 200, 300]), name="lat", cmap=None, units="units")
        with self.assertRaises(AttributeError):
            self.spatial_instrument.add_custom_variable(lat)

        # Test if the variavle already exists and exists_ok = True
        lat = Variable(data=np.array([100, 200, 300]), name="lat", cmap=None, units="units")
        self.spatial_instrument.add_custom_variable(lat,exist_ok=True)
        self.assertEqual(self.spatial_instrument.lat.data.tolist(), [100, 200, 300])


    def test_date2num(self):
        """Test the date2num method."""
        time_var = Variable(data=np.array(["2024-01-01", "2024-01-02"], dtype='datetime64[D]'),
                            name="time", cmap=None, units="units")
        self.spatial_instrument.time = time_var
        date_num = self.spatial_instrument.date2num()
        self.assertEqual(len(date_num), 2)

        # Test if time variable is missing
        self.spatial_instrument.time = None
        with self.assertRaises(ValueError):
            date_num = self.spatial_instrument.date2num()


    def test_repr(self):
        """Test the __repr__ method."""
        self.spatial_instrument = SpatialInstrument()
        self.assertEqual(repr(self.spatial_instrument), "{'bounds': None,\n 'custom_variables': {},\n 'depth': None,\n 'lat': None,\n 'lon': None,\n 'time': None}")

