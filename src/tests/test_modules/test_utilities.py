from gerg_plotting.modules.utilities import to_numpy_array,calculate_range,calculate_pad,print_time,print_datetime,extract_kwargs,extract_kwargs_with_aliases

import unittest
import numpy as np
import io
from unittest.mock import patch
import datetime

class TestToNumpyArray(unittest.TestCase):
    def test_dict_conversion(self):
        """Test that a dictionary is converted to a NumPy array."""
        input_dict = {"a": 1, "b": 2, "c": 3}
        with self.assertRaises(TypeError):
            to_numpy_array(input_dict)
        
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
        self.assertAlmostEqual(result[0], 0.9)
        self.assertAlmostEqual(result[1], 5.1)
        
class TestExtractKwargs(unittest.TestCase):
    def test_extract_kwargs_with_defaults(self):
        # Test case with both provided and default values
        kwargs = {'color': 'blue', 'size': 10}
        defaults = {'color': 'red', 'shape': 'circle', 'size': 5}
        
        result = extract_kwargs(kwargs, defaults)
        
        self.assertEqual(result['color'], 'blue')  # Should use provided value
        self.assertEqual(result['shape'], 'circle')  # Should use default value
        self.assertEqual(result['size'], 10)  # Should use provided value
        self.assertEqual(kwargs, {})  # Original kwargs should be modified

    def test_extract_kwargs_empty(self):
        # Test case with empty kwargs
        kwargs = {}
        defaults = {'color': 'red', 'size': 5}
        
        result = extract_kwargs(kwargs, defaults)
        
        self.assertEqual(result, defaults)  # Should return all default values
        self.assertEqual(kwargs, {})  # Original kwargs should remain empty

    def test_extract_kwargs_no_defaults(self):
        # Test case with no defaults
        kwargs = {'color': 'blue', 'size': 10}
        defaults = {}
        
        result = extract_kwargs(kwargs, defaults)
        
        self.assertEqual(result, {})  # Should return empty dict
        self.assertEqual(kwargs, {'color': 'blue', 'size': 10})  # Original kwargs should be unchanged


class TestExtractKwargsWithAliases(unittest.TestCase):
    def test_basic_extraction(self):
        kwargs = {'color': 'blue', 'size': 10}
        defaults = {('color', 'colour'): 'red', 'size': 5}
        
        result = extract_kwargs_with_aliases(kwargs, defaults)
        
        self.assertEqual(result['color'], 'blue')
        self.assertEqual(result['size'], 10)
        self.assertEqual(kwargs, {})

    def test_alias_extraction(self):
        kwargs = {'colour': 'green'}
        defaults = {('color', 'colour'): 'red'}
        
        result = extract_kwargs_with_aliases(kwargs, defaults)
        
        self.assertEqual(result['color'], 'green')
        self.assertEqual(kwargs, {})

    def test_default_values(self):
        kwargs = {}
        defaults = {('color', 'colour'): 'red', ('size', 'dimension'): 5}
        
        result = extract_kwargs_with_aliases(kwargs, defaults)
        
        self.assertEqual(result['color'], 'red')
        self.assertEqual(result['size'], 5)

    def test_mixed_single_and_tuple_keys(self):
        kwargs = {'width': 100}
        defaults = {
            ('color', 'colour'): 'red',
            'width': 50,
            ('height', 'h'): 30
        }
        
        result = extract_kwargs_with_aliases(kwargs, defaults)
        
        self.assertEqual(result['color'], 'red')
        self.assertEqual(result['width'], 100)
        self.assertEqual(result['height'], 30)
        
class TestPrintTime(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('datetime.datetime')  # Mock datetime.datetime
    def test_print_time(self, mock_datetime, mock_stdout):
        """Test the print_time_simple function to ensure correct output."""

        # Set up the mock to return a fixed datetime
        fixed_time = datetime.datetime(2024, 11, 15, 12, 0, 0)
        mock_datetime.today.return_value = fixed_time
        mock_datetime.strftime = datetime.datetime.strftime

        # Call the function
        message = "Test message"
        print_time(message)

        # Expected output based on the mocked datetime
        expected_output = f"{message}: {fixed_time.strftime('%H:%M:%S')}"

        # Verify the output
        self.assertEqual(mock_stdout.getvalue().rstrip(), expected_output)
        

class TestPrintDateTime(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('datetime.datetime')  # Mock datetime.datetime
    def test_print_time(self, mock_datetime, mock_stdout):
        """Test the print_time_simple function to ensure correct output."""

        # Set up the mock to return a fixed datetime
        fixed_time = datetime.datetime(2024, 11, 15, 12, 0, 0)
        mock_datetime.today.return_value = fixed_time
        mock_datetime.strftime = datetime.datetime.strftime

        # Call the function
        message = "Test message"
        print_datetime(message)

        # Expected output based on the mocked datetime
        expected_output = f"{message}: {fixed_time.strftime('%Y-%m-%d %H:%M:%S')}"

        # Verify the output
        self.assertEqual(mock_stdout.getvalue().rstrip(), expected_output)

