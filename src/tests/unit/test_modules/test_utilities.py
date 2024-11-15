from gerg_plotting.modules.utilities import to_numpy_array,calculate_range,calculate_pad,print_time

import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
import datetime

class TestToNumpyArray(unittest.TestCase):
    def test_dict_conversion(self):
        """Test that a dictionary is converted to a NumPy array."""
        input_dict = {"a": 1, "b": 2, "c": 3}
        result = to_numpy_array(input_dict)
        np.testing.assert_array_equal(result, np.array([1, 2, 3]))

    def test_set_conversion(self):
        """Test that a set is converted to a NumPy array."""
        input_set = {1, 2, 3}
        result = to_numpy_array(input_set)
        np.testing.assert_array_equal(result, np.array([1, 2, 3]))

    def test_list_conversion(self):
        """Test that a list is converted to a NumPy array."""
        input_list = [1, 2, 3]
        result = to_numpy_array(input_list)
        np.testing.assert_array_equal(result, np.array([1, 2, 3]))

    def test_numpy_array_passthrough(self):
        """Test that a NumPy array is returned unchanged."""
        input_array = np.array([1, 2, 3])
        result = to_numpy_array(input_array)
        np.testing.assert_array_equal(result, input_array)

    def test_none_handling(self):
        """Test that None is returned as None."""
        result = to_numpy_array(None)
        self.assertIsNone(result)

    def test_invalid_type(self):
        """Test that invalid types raise a ValueError."""
        with self.assertRaises(ValueError):
            to_numpy_array(42)


class TestCalculateRange(unittest.TestCase):
    def test_calculate_range(self):
        """Test that the range is calculated correctly."""
        input_array = np.array([1, 2, 3, 4, 5])
        result = calculate_range(input_array)
        self.assertEqual(result, [1, 5])

    def test_with_nan_values(self):
        """Test that NaN values are ignored."""
        input_array = np.array([1, np.nan, 3, 4, 5])
        result = calculate_range(input_array)
        self.assertEqual(result, [1, 5])


class TestCalculatePad(unittest.TestCase):
    def test_calculate_pad_no_padding(self):
        """Test that no padding is added when pad=0."""
        input_array = np.array([1, 2, 3, 4, 5])
        result = calculate_pad(input_array, pad=0)
        self.assertEqual(result, (1.0, 5.0))

    def test_calculate_pad_with_padding(self):
        """Test that padding is added correctly."""
        input_array = np.array([1, 2, 3, 4, 5])
        result = calculate_pad(input_array, pad=0.1)
        self.assertAlmostEqual(result[0], 0.6)
        self.assertAlmostEqual(result[1], 5.4)


class TestPrintTime(unittest.TestCase):
    @patch("builtins.print")
    @patch("datetime.datetime")
    def test_print_time_no_value(self, mock_datetime, mock_print):
        """Test printing the current time when value is None."""
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)
        print_time()
        mock_print.assert_called_once_with("12:00:00")

    @patch("builtins.print")
    @patch("datetime.datetime")
    def test_print_time_value_within_interval(self, mock_datetime, mock_print):
        """Test printing when value is within intervals."""
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)
        print_time(value=10, intervals=[10, 50, 100])
        mock_print.assert_called_once_with("value = 10, 12:00:00")

    def test_print_time_invalid_intervals(self):
        """Test that invalid intervals raise a ValueError."""
        with self.assertRaises(ValueError):
            print_time(value=10, intervals=[10])

    @patch("builtins.print")
    @patch("datetime.datetime")
    def test_print_time_large_value(self, mock_datetime, mock_print):
        """Test printing when value is larger than the last interval."""
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)
        print_time(value=5000, intervals=[10, 50, 100, 500, 1000])
        mock_print.assert_called_once_with("value = 5000, 12:00:00")

