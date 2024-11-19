
import unittest
import pandas as pd
import numpy as np
import xarray as xr
from io import StringIO
import os
from pathlib import Path

from gerg_plotting.data_classes.Data import Data
from gerg_plotting.tools import _map_variables, _get_var_mapping, interp_glider_lat_lon, data_from_df, data_from_csv


# Sample dataset for testing
def create_test_dataset():
    """
    Creates a test dataset with variables 'time', 'm_time', 'latitude', and 'longitude'.
    Includes NaN values for latitude and longitude to test interpolation.
    """
    time = np.array(['2023-01-01T00:00:00', '2023-01-01T01:00:00', '2023-01-01T02:00:00'], dtype='datetime64[ns]')
    m_time = np.array(['2023-01-01T00:00:00', '2023-01-01T01:30:00', '2023-01-01T02:00:00'], dtype='datetime64[ns]')
    
    latitude = np.array([34.0, np.nan, 36.0])  # Include NaN to test interpolation
    longitude = np.array([-120.0, np.nan, -118.0])  # Include NaN to test interpolation
    
    ds = xr.Dataset(
        {
            'latitude': (['m_time'], latitude),
            'longitude': (['m_time'], longitude),
            'time': (['time'], time),
            'm_time': (['m_time'], m_time),
        }
    )
    return ds


class TestFunctions(unittest.TestCase):

    def tearDown(self):
        if Path('test.csv').exists():
            os.remove('test.csv')

    def test_map_variables(self):
        keys = ['depth', 'temperature', 'u', 's']
        values = ['pres', 'temp', 'eastward_velocity', 'speed', 'sound_speed']

        synonyms = {
            'depth': ['pressure', 'pres'],
            'temperature': ['temp', 'temperature_measure'],
            'salinity': ['salt', 'salinity_level'],
            'density': ['density_metric', 'rho'],
            'u': ['eastward_velocity', 'u_component'],
            'v': ['northward_velocity', 'v_component'],
            'w': ['downward_velocity','upward_velocity','w_component'],
            's': ['combined_velocity','velocity','speed']
        }
        blocklist = {
            's': ['sound','pres']
        }

        expected_output = {
            'depth': 'pres',
            'temperature': 'temp',
            'u': 'eastward_velocity',
            's': 'speed'
        }

        self.assertEqual(_map_variables(keys, values,synonyms,blocklist), expected_output,msg=f'{_map_variables(keys,values,synonyms,blocklist) = }')

    def test_get_var_mapping(self):
        df = pd.DataFrame(columns=['pres', 'temp', 'eastward_velocity', 'speed', 'latitude', 'longitude'])
        expected_output = {
            'lat': 'latitude',
            'lon': 'longitude',
            'depth': 'pres',
            'time': None,
            'temperature': 'temp',
            'salinity': None,
            'density': None,
            'u': 'eastward_velocity',
            'v': None,
            'w': None,
            'speed': 'speed'
        }

        self.assertEqual(_get_var_mapping(df), expected_output,msg=f'{_get_var_mapping(df) = }')

    def test_interpolation(self):
        """Test interpolation of latitude and longitude in the function."""
        # Create the test dataset
        ds = create_test_dataset()

        # Call the function
        interpolated_ds = interp_glider_lat_lon(ds)

        # Check that 'm_time' was removed
        self.assertNotIn('m_time', interpolated_ds)

        # Verify 'latitude' interpolation
        expected_latitude = np.array([34.0, 35.0, 36.0])
        np.testing.assert_almost_equal(interpolated_ds['latitude'].values, expected_latitude)

        # Verify 'longitude' interpolation
        expected_longitude = np.array([-120.0, -119.0, -118.0])
        np.testing.assert_almost_equal(interpolated_ds['longitude'].values, expected_longitude)

        # Check dimensions and coordinates of the output dataset
        self.assertIn('time', interpolated_ds.dims)
        self.assertEqual(len(interpolated_ds['time']), 3)
        self.assertEqual(interpolated_ds['latitude'].dims, ('time',))
        self.assertEqual(interpolated_ds['longitude'].dims, ('time',))

    def test_data_from_df(self):
        df = pd.DataFrame({
            'lat': [10, 20, 30],
            'lon': [40, 50, 60],
            'depth': [100, 200, 300]
        })
        mapped_variables = {
            'lat': 'lat',
            'lon': 'lon',
            'depth': 'depth'
        }

        data = data_from_df(df, mapped_variables)

        # Assert the Data object has the expected attributes
        self.assertEqual(data.lat.data.tolist(), [10, 20, 30])
        self.assertEqual(data.lon.data.tolist(), [40, 50, 60])
        self.assertEqual(data.depth.data.tolist(), [100, 200, 300])

    def test_data_from_csv(self):
        csv_data = """lat,lon,depth
                        10,40,100
                        20,50,200
                        30,60,300"""
        filename = "test.csv"
        with open(filename, "w") as file:
            file.write(csv_data)

        mapped_variables = {
            'lat': 'lat',
            'lon': 'lon',
            'depth': 'depth'
        }

        data = data_from_csv(filename, mapped_variables)

        # Assert the Data object has the expected attributes
        self.assertEqual(data.lat.data.tolist(), [10, 20, 30])
        self.assertEqual(data.lon.data.tolist(), [40, 50, 60])
        self.assertEqual(data.depth.data.tolist(), [100, 200, 300])


