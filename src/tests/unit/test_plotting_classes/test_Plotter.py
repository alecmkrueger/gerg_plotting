import unittest
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.colors import Colormap
import numpy as np
from attrs import define,field

from gerg_plotting.plotting_classes.Plotter import Plotter

@define
class DummyVariable:
    """Dummy variable class with minimal attributes for testing."""
    cmap: Colormap = None

    def get_label(self):
        return "Dummy Variable"

@define
class DummyData:
    """Dummy Data class to simulate Plotter dependencies."""
    variables: dict = field(factory=dict)

    def __getitem__(self, key):
        return self.variables[key]

class TestPlotter(unittest.TestCase):
    def setUp(self):
        # Create a DummyData instance with a dummy variable
        dummy_var = DummyVariable(cmap=plt.get_cmap('viridis'))
        dummy_time_var = DummyVariable(cmap=plt.get_cmap('viridis'))
        self.data = DummyData(variables={'test_var': dummy_var,'time':dummy_time_var})
        self.plotter = Plotter(data=self.data)
        # Fake the cbar attribute
        self.plotter.cbar = None

    def tearDown(self):
        plt.close()

    def test_setitem(self):
        with self.assertRaises(KeyError):
            self.plotter['nonexistent']

    def test_init_figure_2d(self):
        """Test initializing a standard 2D figure."""
        self.plotter.init_figure(figsize=(8, 6))
        self.assertIsInstance(self.plotter.fig, Figure)
        self.assertIsInstance(self.plotter.ax, Axes)
        self.assertEqual(self.plotter.fig.get_size_inches().tolist(), [8, 6])

    def test_init_figure_geography(self):
        """Test initializing a figure with geographic projection."""
        self.plotter.init_figure(geography=True)
        self.assertIsNotNone(self.plotter.ax.projection)

    def test_init_figure_3d(self):
        """Test initializing a 3D figure."""
        self.plotter.init_figure(three_d=True)
        self.assertEqual(self.plotter.ax.name, '3d')

    def test_init_figure_3d_and_geography(self):
        """Test initializing a 3D with geography figure."""
        with self.assertRaises(ValueError):
            self.plotter.init_figure(three_d=True,geography=True)

    def test_init_figure_3d_with_existing_axes(self):
        """Test initializing a 3D figure."""
        fig,ax = plt.subplots()
        self.plotter.init_figure(fig=fig,ax=ax,three_d=True)
        self.assertEqual(self.plotter.ax.name, '3d')

    def test_get_cmap(self):
        """Test retrieving a colormap for a variable."""
        cmap = self.plotter.get_cmap('test_var')
        self.assertIsInstance(cmap, Colormap)
        self.assertEqual(cmap.name, 'viridis')

    def test_get_cmap_missing_cmap(self):
        """Test retrieving a colormap for a variable."""
        test_data = self.data
        test_data['test_var'].cmap = None
        self.plotter.data = test_data
        cmap = self.plotter.get_cmap('test_var')
        self.assertIsInstance(cmap, Colormap)
        self.assertEqual(cmap.name, 'viridis')

    def test_add_colorbar(self):
        """Test adding a colorbar."""
        self.plotter.init_figure()
        scatter = self.plotter.ax.scatter([1, 2, 3], [4, 5, 6], c=[0.1, 0.5, 0.9])
        cbar = self.plotter.add_colorbar(mappable=scatter, var='test_var')
        self.assertIsInstance(cbar, Colorbar)
        self.assertEqual(cbar.ax.get_ylabel(), 'Dummy Variable')

    def test_add_colorbar_with_time(self):
        """Test adding a colorbar."""
        self.plotter.init_figure()
        scatter = self.plotter.ax.scatter([1, 2, 3], [4, 5, 6], c=[0.1, 0.5, 0.9])
        cbar = self.plotter.add_colorbar(mappable=scatter, var='time')
        self.assertIsInstance(cbar, Colorbar)
        self.assertEqual(cbar.ax.get_ylabel(), 'Dummy Variable')

    def test_format_axes(self):
        """Test formatting the axes."""
        self.plotter.init_figure()
        self.plotter.format_axes('X Axis', 'Y Axis', invert_yaxis=True)
        self.assertEqual(self.plotter.ax.get_xlabel(), 'X Axis')
        self.assertEqual(self.plotter.ax.get_ylabel(), 'Y Axis')
        self.assertTrue(self.plotter.ax.yaxis_inverted())

    def test_dict_access(self):
        """Test dictionary-style access."""
        self.plotter['bounds_padding'] = 10
        self.assertEqual(self.plotter['bounds_padding'], 10)
        with self.assertRaises(KeyError):
            _ = self.plotter['nonexistent']

    def test_repr(self):
        """Test the string representation of the class."""
        repr_str = repr(self.plotter)
        self.assertIn('bounds_padding', repr_str)

    def test_get_vars(self):
        """Test retrieving a list of variables."""
        vars_list = self.plotter.get_vars()
        self.assertIn('data', vars_list)
        self.assertIn('fig', vars_list)

