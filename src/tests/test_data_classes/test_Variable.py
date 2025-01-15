import unittest
import numpy as np
from gerg_plotting.data_classes.variable import Variable


class TestVariable(unittest.TestCase):

    def setUp(self):
        """Set up test data for the tests."""
        self.data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.variable_name = "temperature"
        self.units = "C"
        self.variable = Variable(data=self.data, name=self.variable_name, units=self.units)

    def test_initialization(self):
        """Test initialization of Variable class."""
        self.assertTrue(np.array_equal(self.variable.data, self.data))
        self.assertEqual(self.variable.name, self.variable_name)
        self.assertEqual(self.variable.units, self.units)
        self.assertEqual(self.variable.vmin, np.nanpercentile(self.data, 1))
        self.assertEqual(self.variable.vmax, np.nanpercentile(self.data, 99))

    def test_label_generation(self):
        """Test automatic generation of the label."""
        label = self.variable.get_label()
        self.assertEqual(label, f"{self.variable_name.capitalize()} ({self.units})")

    def test_label_custom(self):
        """Test custom label assignment."""
        custom_label = "Custom Label"
        self.variable.label = custom_label
        self.assertEqual(self.variable.get_label(), custom_label)
        
    def test_get_and_reset_label(self):
        """Test resetting the label to the default."""
        self.variable.get_label()
        self.assertEqual(self.variable.get_label(), f"{self.variable_name.capitalize()} ({self.units})")
        self.variable.reset_label()
        self.assertIsNone(self.variable.label)
            
    def test_format_value(self):
        """Test _format_value method with different data types."""
        # Test float formatting
        self.assertEqual(self.variable._format_value(3.14159), "3.141590")
        
        # Test datetime formatting
        test_date = np.datetime64('2023-01-15T14:30:45.123')
        expected_date = "23-01-15 14:30:45"
        self.assertEqual(self.variable._format_value(test_date), expected_date)
        
        # Test Python datetime
        from datetime import datetime
        py_date = datetime(2023, 1, 15, 14, 30, 45)
        self.assertEqual(self.variable._format_value(py_date), "23-01-15 14:30:45")
        
        # Test colormap
        from matplotlib.cm import viridis
        self.assertEqual(self.variable._format_value(viridis), "viridis")
        
        # Test string
        self.assertEqual(self.variable._format_value("test"), "test")

    def test_repr_html(self):
        """Test _repr_html_ method output structure."""
        html_output = self.variable._repr_html_()
        
        # Test that HTML output is a string
        self.assertIsInstance(html_output, str)
        
        # Test essential HTML elements are present
        self.assertIn("<table", html_output)
        self.assertIn("</table>", html_output)
        self.assertIn("<tbody>", html_output)
        self.assertIn("</tbody>", html_output)
        
        # Test that all attributes are represented
        for attr in self.variable.get_attrs():
            if attr != 'data':  # Skip data as it's handled separately
                self.assertIn(attr, html_output)
        
        # Test data section exists
        self.assertIn("Length: 5", html_output)  # Our test data has 5 elements
        
        # Test sample data values are present
        for i in range(min(5, len(self.data))):
            self.assertIn(str(self.data[i]), html_output)


    def test_getitem(self):
        """Test __getitem__ for accessing attributes."""
        self.assertEqual(self.variable["name"], self.variable_name)
        self.assertTrue(np.array_equal(self.variable["data"], self.data))
        with self.assertRaises(KeyError):
            _ = self.variable["non_existent"]

    def test_setitem(self):
        """Test __setitem__ for updating attributes."""
        new_units = "K"
        self.variable["units"] = new_units
        self.assertEqual(self.variable.units, new_units)
        with self.assertRaises(KeyError):
            self.variable["non_existent"] = "value"

    def test_get_attrs(self):
        """Test retrieval of attribute names."""
        attrs = self.variable.get_attrs()
        expected_attrs = ['data', 'name', 'cmap', 'units', 'vmin', 'vmax', 'label']
        self.assertCountEqual(attrs, expected_attrs)

    def test_repr(self):
        """Test the string representation."""
        representation = repr(self.variable)
        # Ensure the name is in the representation
        self.assertIn(self.variable_name, representation)
        # Ensure the data is correctly represented as a numpy array
        expected_data_repr = repr(self.data)  # Generate the expected array representation
        self.assertIn(expected_data_repr, representation)


    def test_vmin_vmax_calculation(self):
        """Test automatic calculation of vmin and vmax."""
        self.variable.vmin = None
        self.variable.vmax = None
        self.variable.get_vmin_vmax()
        self.assertEqual(self.variable.vmin, np.nanpercentile(self.data, 1))
        self.assertEqual(self.variable.vmax, np.nanpercentile(self.data, 99))

