from gerg_plotting.modules.filters import filter_var,filter_nan

import unittest
import numpy as np
import pandas as pd
import xarray as xr


class TestFilterVarFunction(unittest.TestCase):
    def test_filter_var_xarray(self):
        # Test with xarray.DataArray
        data = xr.DataArray([1, 2, 3, 4, 5])
        result = filter_var(data, 2, 4)
        expected = xr.DataArray([np.nan, 2, 3, 4, np.nan])
        xr.testing.assert_equal(result, expected)

    def test_filter_var_numpy_array(self):
        # Test with numpy array
        data = np.array([1, 2, 3, 4, 5])
        result = filter_var(data, 2, 4)
        expected = np.array([np.nan, 2, 3, 4, np.nan])
        np.testing.assert_array_equal(result, expected)

    def test_filter_var_pandas_series(self):
        # Test with pandas Series
        data = pd.Series([1, 2, 3, 4, 5])
        result = filter_var(data, 2, 4)
        expected = pd.Series([np.nan, 2, 3, 4, np.nan])
        pd.testing.assert_series_equal(result, expected)

    def test_filter_var_list(self):
        # Test with a list
        data = [1, 2, 3, 4, 5]
        result = filter_var(data, min_value=2, max_value=4)
        expected = [np.nan, 2, 3, 4, np.nan]
        self.assertEqual(result, expected)

    def test_filter_var_invalid_type(self):
        # Test with unsupported type
        data = "invalid"
        with self.assertRaises(TypeError):
            filter_var(data, 2, 4)


class TestFilterNanFunction(unittest.TestCase):
    def test_filter_nan_numpy_array(self):
        # Test with numpy array
        data = np.array([1, np.nan, 2, np.nan, 3])
        result = filter_nan(data)
        expected = np.array([1, 2, 3])
        np.testing.assert_array_equal(result, expected)

    def test_filter_nan_pandas_series(self):
        # Test with pandas Series
        data = pd.Series([1, np.nan, 2, np.nan, 3])
        result = filter_nan(data)
        expected = pd.Series([1.0, 2.0, 3.0], index=[0, 2, 4])
        pd.testing.assert_series_equal(result, expected)

    def test_filter_nan_xarray_dataarray(self):
        # Test with xarray.DataArray
        data = xr.DataArray([1, np.nan, 2, np.nan, 3])
        result = filter_nan(data)
        expected = xr.DataArray([1, 2, 3])
        xr.testing.assert_equal(result, expected)

    def test_filter_nan_list(self):
        # Test with a list
        data = [1, np.nan, 2, np.nan, 3]
        result = filter_nan(data)
        expected = [1, 2, 3]
        self.assertEqual(result, expected)

    def test_filter_nan_invalid_type(self):
        # Test with unsupported type
        data = "invalid"
        with self.assertRaises(TypeError):
            filter_nan(data)

    def test_filter_nan_no_nan_values(self):
        # Test when there are no NaN values
        data = np.array([1, 2, 3, 4, 5])
        result = filter_nan(data)
        expected = np.array([1, 2, 3, 4, 5])
        np.testing.assert_array_equal(result, expected)

    def test_filter_nan_all_nan_values(self):
        # Test when all values are NaN
        data = np.array([np.nan, np.nan, np.nan])
        result = filter_nan(data)
        expected = np.array([])
        np.testing.assert_array_equal(result, expected)

