import unittest
import pandas as pd
from gerg_plotting import Data, Variable
from gerg_plotting.examples.data_object_example import (
    read_example_data,
    create_data_with_iterables,
    create_variable_objects,
    create_data_with_variables,
    modify_data_attributes,
    add_custom_variable,
    create_data_from_csv,
    create_data_from_df
)


class TestDataObjectFunctions(unittest.TestCase):
    def setUp(self):
        """Set up sample data for testing."""
        self.sample_data = {
            'latitude': [27.0, 27.5, 28.0],
            'longitude': [-95.0, -95.5, -96.0],
            'pressure': [10, 20, 30],
            'time': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'salinity': [35, 36, 37],
            'temperature': [15, 16, 17],
            'density': [1025, 1026, 1027],
            'Turner_Rsubrho': [0.5, 0.6, 0.7]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_read_example_data(self):
        """Test reading data from a CSV file."""
        self.df.to_csv('test_data.csv', index=False)
        df = read_example_data('test_data.csv')
        self.assertEqual(len(df), len(self.df))
        self.assertTrue((df['latitude'] == self.df['latitude']).all())
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['time']))

    def test_create_data_from_csv(self):
        """Test creating a Data object from a CSV file."""
        self.df.to_csv('test_data.csv', index=False)
        data = create_data_from_csv('test_data.csv')
        self.assertIsInstance(data, Data)
        self.assertEqual(len(data.lat.data), len(self.df['latitude']))
        self.assertTrue(hasattr(data, 'temperature'))

    def test_create_data_from_df(self):
        """Test creating a Data object directly from a DataFrame."""
        data = create_data_from_df(self.df)
        self.assertIsInstance(data, Data)
        self.assertEqual(len(data.lat.data), len(self.df['latitude']))
        self.assertTrue(hasattr(data, 'salinity'))

    def test_create_data_with_iterables(self):
        """Test creating a Data object using iterables."""
        data = create_data_with_iterables(self.df)
        self.assertIsInstance(data, Data)
        self.assertTrue(hasattr(data, 'lat'))
        self.assertEqual(len(data.lat.data), len(self.df['latitude']))

    def test_create_variable_objects(self):
        """Test creating Variable objects."""
        vars = create_variable_objects(self.df)
        self.assertEqual(len(vars), 7)
        for var in vars:
            self.assertIsInstance(var, Variable)

    def test_create_data_with_variables(self):
        """Test creating a Data object using Variable objects."""
        vars = create_variable_objects(self.df)
        data = create_data_with_variables(*vars)
        self.assertIsInstance(data, Data)
        self.assertTrue(hasattr(data, 'temperature'))
        self.assertEqual(len(data.temperature.data), len(self.df['temperature']))

    def test_modify_data_attributes(self):
        """Test modifying attributes of variables in a Data object."""
        vars = create_variable_objects(self.df)
        data = create_data_with_variables(*vars)
        modified_data = modify_data_attributes(data)
        self.assertEqual(modified_data['lat'].vmin, 27)
        self.assertEqual(modified_data['depth'].units, 'km')

    def test_add_custom_variable(self):
        """Test adding a custom variable to a Data object."""
        vars = create_variable_objects(self.df)
        data = create_data_with_variables(*vars)
        updated_data = add_custom_variable(data, self.df, 'Turner_Rsubrho')
        self.assertIn('Turner_Rsubrho', updated_data.custom_variables)
        self.assertEqual(updated_data['Turner_Rsubrho'].name, 'Turner_Rsubrho')
        self.assertEqual(len(updated_data['Turner_Rsubrho'].data), len(self.df['Turner_Rsubrho']))

    def tearDown(self):
        """Clean up after tests."""
        import os
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')

