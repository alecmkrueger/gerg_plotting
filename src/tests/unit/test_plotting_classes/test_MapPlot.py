import unittest
import matplotlib.pyplot as plt
import numpy as np
from gerg_plotting.data_classes.Bathy import Bathy
from gerg_plotting.plotting_classes.MapPlot import MapPlot
from gerg_plotting.tools import data_from_csv

class TestMapPlot(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test environment for MapPlot.
        """

        self.data = data_from_csv('C:/Users/alecmkrueger/Documents/GERG/gerg_plotting/src/gerg_plotting/examples/example_data/sample_glider_data.csv')
        
        # Create a MapPlot instance with a mock bathymetry object
        self.map_plot = MapPlot(data=self.data)


    def test_init_bathy(self):
        """
        Test the initialization of bathymetry in the MapPlot class.
        """
        # When no bathy is provided, it should set the bathy attribute to a Bathy instance
        self.map_plot.bathy = None
        self.map_plot.init_bathy()
        self.assertIsInstance(self.map_plot.bathy, Bathy)

    def test_set_up_map(self):
        """
        Test the setup of the map, including color mapping and extent settings.
        """
        # Test with a variable (e.g., 'temperature')
        var = 'temperature'
        color, cmap, divider = self.map_plot.set_up_map(var=var)
        
        self.assertIsInstance(color, np.ndarray)
        self.assertIsNotNone(cmap)  # Colormap should not be None
        self.assertIsNotNone(divider)  # Divider should not be None

    def test_add_coasts(self):
        """
        Test adding coastlines to the map.
        """
        self.map_plot.add_coasts(show_coastlines=True)
        # Check if the coastlines have been added
        self.assertTrue(self.map_plot.ax.has_data())  # This is a very basic check for coastlines

    def test_add_grid(self):
        """
        Test adding gridlines to the map.
        """
        self.map_plot.add_grid(grid=True)
        # Check if the gridlines have been added
        self.assertTrue(self.map_plot.gl)  # The gridliner object should exist

    def test_add_bathy(self):
        """
        Test adding bathymetric data to the map.
        """
        divider = self.map_plot.set_up_map('temperature')[2]
        self.map_plot.add_bathy(show_bathy=True, divider=divider)
        # Check if bathymetry has been added to the axis
        self.assertIsNotNone(self.map_plot.cbar_bathy)  # Colorbar for bathymetry should exist

    def test_scatter(self):
        """
        Test the scatter plot method in MapPlot.
        """
        self.map_plot.scatter(var='temperature', show_bathy=True, show_coastlines=True)
        # Check that the scatter plot has been created
        self.assertIsNotNone(self.map_plot.sc)  # PathCollection for scatter plot should exist
        self.assertIsNotNone(self.map_plot.cbar_var)  # Colorbar for scatter variable should exist

    def test_quiver(self):
        """
        Test the quiver plot method in MapPlot.
        """
        self.map_plot.quiver(x='lon', y='lat', quiver_density=10, quiver_scale=1.0)
        # Check that the quiver plot has been created
        self.assertIsNotNone(self.map_plot.cbar_var)  # Colorbar for quiver speed should exist
        self.assertTrue(hasattr(self.map_plot, 'sc'))  # Check for scatter plot presence (even if not created directly)

    def tearDown(self):
        """
        Clean up after each test.
        """
        plt.close(self.map_plot.fig)

