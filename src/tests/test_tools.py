import unittest
import numpy as np
import pandas as pd
import xarray as xr
import tempfile
import os
from gerg_plotting.tools.tools import (
    normalize_string,
    merge_dicts,
    create_combinations_with_underscore,
    _map_variables,
    _get_var_mapping,
    data_from_df,
    custom_legend_handles,
    interp_glider_lat_lon,
    data_from_csv,
    data_from_ds,
    data_from_netcdf
)

class TestTools(unittest.TestCase):
    def test_normalize_string(self):
        # Test basic normalization
        self.assertEqual(normalize_string("Hello World!"), "hello_world")
        # Test multiple special characters
        self.assertEqual(normalize_string("temp@#$%^&*()"), "temp")
        # Test multiple spaces and special chars
        self.assertEqual(normalize_string("  temp  value  "), "temp_value")
        # Test empty string
        self.assertEqual(normalize_string(""), "")
        # Test with numbers
        self.assertEqual(normalize_string("temp123"), "temp123")
        
        with self.assertRaises(ValueError):
            normalize_string(123)

    def test_merge_dicts(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'b': 3, 'c': 4}
        dict3 = {'d': 5}
        
        # Test merging two dictionaries
        self.assertEqual(merge_dicts(dict1, dict2), {'a': 1, 'b': 3, 'c': 4})
        # Test merging three dictionaries
        self.assertEqual(merge_dicts(dict1, dict2, dict3), {'a': 1, 'b': 3, 'c': 4, 'd': 5})
        # Test merging with empty dict
        self.assertEqual(merge_dicts(dict1, {}), dict1)

    def test_create_combinations_with_underscore(self):
        strings = ['temp', 'sal', 'depth']
        result = create_combinations_with_underscore(strings)
        
        expected_combinations = ['temp_sal', 'temp_depth', 'sal_depth', 'temp', 'sal', 'depth']
        self.assertEqual(sorted(result), sorted(expected_combinations))
        
        # Test with single string
        self.assertEqual(create_combinations_with_underscore(['temp']), ['temp'])
        
        # Test with empty list
        self.assertEqual(create_combinations_with_underscore([]), [])

    def test_custom_legend_handles(self):
        # Test basic legend handles
        labels = ['temp_1', 'sal_2']
        colors = ['red', 'blue']
        result = custom_legend_handles(labels, colors)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].get_label(), 'temp/1')
        self.assertEqual(result[0].get_facecolor(), (1.0, 0.0, 0.0, 1.0))  # red

        # Test with hatches
        hatches = ['/', '\\']
        result_hatched = custom_legend_handles(labels, colors, hatches=hatches)
        self.assertEqual(result_hatched[0].get_hatch(), '/')
        
        # Test with color_hatch_not_background
        result_hatch_color = custom_legend_handles(labels, colors, hatches=hatches, color_hatch_not_background=True)
        self.assertEqual(result_hatch_color[0].get_facecolor(), (0, 0, 0, 0))  # transparent
        self.assertEqual(result_hatch_color[0].get_edgecolor(), (1.0, 0.0, 0.0, 1.0))  # red


    def test_map_variables(self):
        keys = ['temp', 'sal']
        values = ['temperature', 'salinity', 'depth']
        synonyms = {'temp': ['temperature'], 'sal': ['salinity']}
        
        result = _map_variables(keys, values, synonyms)
        
        self.assertEqual(result['temp'], 'temperature')
        self.assertEqual(result['sal'], 'salinity')

        # Test with blocklist
        blocklist = {'temp': ['air']}
        values_with_air = ['air_temperature', 'temperature', 'salinity']
        result = _map_variables(keys, values_with_air, synonyms, blocklist)
        self.assertEqual(result['temp'], 'temperature')
        
    def test_map_variables_single_letters(self):
        # Test single letter variables (u, v, w, s)
        keys = ['u', 'v', 'w', 's']
        values = ['u_velocity', 'v_current', 'w_component', 'speed']
        synonyms = {
            'u': ['u_component', 'u_current'],
            'v': ['v_component', 'v_current'],
            'w': ['w_component', 'w_current'],
            's': ['speed', 'combined_velocity']
        }
        
        result = _map_variables(keys, values, synonyms)
        
        # Test exact matches
        self.assertEqual(result['u'], 'u_velocity')
        self.assertEqual(result['v'], 'v_current')
        self.assertEqual(result['w'], 'w_component')
        self.assertEqual(result['s'], 'speed')
        
        # Test with values that start with single letter
        values_start = ['u_data', 'velocity_v', 'w_speed', 'sound_speed']
        blocklist = {'s': ['sound']}
        result_start = _map_variables(keys, values_start, synonyms, blocklist)
        
        self.assertEqual(result_start['u'], 'u_data')
        self.assertIsNone(result_start['s'])  # Should be None due to blocklist
        
    def test_map_variables_single_letter_exact_match(self):
        # Test single letter variables (u, v, w, s)
        keys = ['u', 'v', 'w', 's', 'd','t','c','vd']
        values = ['u_velocity', 'v_current', 'w_component', 'speed', 'd','theta','variable_c','v_direction']
        synonyms = {
            't': ['theta'],
            'c': ['variable_c'],
            'vd':['v_direction']
        }

        result = _map_variables(keys, values, synonyms)

        # Test exact matches
        self.assertEqual(result['d'], 'd')
        self.assertEqual(result['t'], 'theta')
        self.assertEqual(result['c'], 'variable_c')


    def test_get_var_mapping(self):
        df = pd.DataFrame({
            'temperature': [20, 21],
            'salinity': [35, 36],
            'pressure': [10, 11]
        })
        
        result = _get_var_mapping(df)
        
        self.assertIn('temperature', result)
        self.assertIn('salinity', result)
        self.assertEqual(result['depth'], 'pressure')

    def test_interp_glider_lat_lon(self):
        # Create test dataset
        times = pd.date_range('2023-01-01', '2023-01-02', periods=5)
        m_times = pd.date_range('2023-01-01', '2023-01-02', periods=5)
        
        ds = xr.Dataset(
            {
                'latitude': ('time', [25.0, np.nan, 26.0, np.nan, 27.0]),
                'longitude': ('time', [-90.0, np.nan, -91.0, np.nan, -92.0]),
                'm_time': ('time', m_times)
            },
            coords={'time': times}
        )
        
        result = interp_glider_lat_lon(ds)
        
        # Test interpolation results
        self.assertFalse(np.any(np.isnan(result.latitude)))
        self.assertFalse(np.any(np.isnan(result.longitude)))
        self.assertNotIn('m_time', result)

    def test_data_from_df_full(self):
        # Create test dataframe
        df = pd.DataFrame({
            'latitude': [25, 26],
            'longitude': [-90, -91],
            'temperature': [20, 21],
            'depth': [100, 200],
            'time': pd.date_range('2023-01-01', '2023-01-02')
        })
        
        # Test with automatic variable mapping
        result = data_from_df(df)
        self.assertTrue(hasattr(result, 'lat'))
        self.assertTrue(hasattr(result, 'lon'))
        self.assertTrue(hasattr(result, 'temperature'))
        self.assertTrue(hasattr(result, 'depth'))
        self.assertTrue(hasattr(result, 'time'))

    def test_data_from_csv(self):
        # Create temporary CSV file
        test_df = pd.DataFrame({
            'lat': [25, 26],
            'lon': [-90, -91],
            'temp': [20, 21]
        })
        
        with tempfile.NamedTemporaryFile(suffix='.csv', mode='w', delete=False) as f:
            test_df.to_csv(f.name, index=False)
            
            # Test reading from CSV
            result = data_from_csv(f.name)
            self.assertTrue(hasattr(result, 'lat'))
            self.assertTrue(hasattr(result, 'lon'))
            
            # Test with custom mapping
            mapped_result = data_from_csv(f.name, mapped_variables={'temperature': 'temp'})
            self.assertTrue(hasattr(mapped_result, 'temperature'))
        
        os.remove(f.name)
        
    def test_data_from_ds(self):
        # Create test xarray dataset
        ds = xr.Dataset(
            {
                'latitude': ('time', [25.0, 26.0, 27.0]),
                'longitude': ('time', [-90.0, -91.0, -92.0]),
                'temperature': ('time', [20.0, 21.0, 22.0]),
                'depth': ('time', [100, 200, 300]),
                'time': pd.date_range('2023-01-01', '2023-01-03')
            }
        )
        
        # Test with automatic variable mapping
        result = data_from_ds(ds)
        self.assertTrue(hasattr(result, 'lat'))
        self.assertTrue(hasattr(result, 'lon'))
        self.assertTrue(hasattr(result, 'temperature'))
        self.assertTrue(hasattr(result, 'depth'))
        self.assertTrue(hasattr(result, 'time'))
        
        # Test with custom mapping
        custom_mapping = {'temperature': 'temperature', 'depth': 'depth'}
        result_custom = data_from_ds(ds, mapped_variables=custom_mapping)
        self.assertTrue(hasattr(result_custom, 'temperature'))
        self.assertTrue(hasattr(result_custom, 'depth'))

    def test_data_from_netcdf(self):
        # Create temporary NetCDF file
        ds = xr.Dataset(
            {
                'latitude': ('time', [25.0, 26.0, 27.0]),
                'longitude': ('time', [-90.0, -91.0, -92.0]),
                'temperature': ('time', [20.0, 21.0, 22.0])
            },
            coords={'time': pd.date_range('2023-01-01', '2023-01-03')}
        )
        
        with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as f:
            ds.to_netcdf(f.name)
            
            # Test reading from NetCDF
            result = data_from_netcdf(f.name)
            self.assertTrue(hasattr(result, 'lat'))
            self.assertTrue(hasattr(result, 'lon'))
            self.assertTrue(hasattr(result, 'temperature'))
            
            # Test with custom mapping
            mapped_result = data_from_netcdf(f.name, mapped_variables={'temperature': 'temperature'})
            self.assertTrue(hasattr(mapped_result, 'temperature'))
            
            # Test with glider interpolation
            glider_result = data_from_netcdf(f.name, interp_glider=False)
            self.assertTrue(hasattr(glider_result, 'lat'))
            self.assertTrue(hasattr(glider_result, 'lon'))
        
        os.remove(f.name)


