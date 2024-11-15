import unittest
import numpy as np
from matplotlib.colors import Colormap
from gerg_plotting.data_classes.Variable import Variable


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
        self.assertEqual(self.variable.vmin, np.min(self.data))
        self.assertEqual(self.variable.vmax, np.max(self.data))

    def test_label_generation(self):
        """Test automatic generation of the label."""
        label = self.variable.get_label()
        self.assertEqual(label, f"{self.variable_name.capitalize()} ({self.units})")

    def test_label_custom(self):
        """Test custom label assignment."""
        custom_label = "Custom Label"
        self.variable.label = custom_label
        self.assertEqual(self.variable.get_label(), custom_label)

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
        self.assertEqual(self.variable.vmin, np.min(self.data))
        self.assertEqual(self.variable.vmax, np.max(self.data))

