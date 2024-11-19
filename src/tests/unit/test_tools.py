
import unittest
import pandas as pd
import numpy as np
import xarray as xr
from io import StringIO
import os
from pathlib import Path

from gerg_plotting.data_classes.Data import Data
from gerg_plotting.tools import _map_variables, _get_var_mapping, interp_glider_lat_lon, data_from_df, data_from_csv


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

    def test_interp_glider_lat_lon(self):
        # Create a sample dataset
        ds = xr.Dataset({
            'time': ('time', pd.date_range("2023-01-01", periods=5)),
            'm_time': ('time', pd.date_range("2023-01-01", periods=5).shift(-1)),
            'latitude': ('time', [10, np.nan, 15, np.nan, 20]),
            'longitude': ('time', [30, 35, np.nan, np.nan, 50])
        })

        result = interp_glider_lat_lon(ds)

        # Assert lat/lon are interpolated correctly
        np.testing.assert_allclose(
            result['latitude'].values,
            [10, 12.5, 15, 17.5, 20],
            rtol=1e-5
        )
        np.testing.assert_allclose(
            result['longitude'].values,
            [30, 35, 40, 45, 50],
            rtol=1e-5
        )

        # Assert 'm_time' is dropped
        self.assertNotIn('m_time', result)

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


