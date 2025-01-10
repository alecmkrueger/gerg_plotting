from gerg_plotting.plotting_classes.Histogram import Histogram
from gerg_plotting.data_classes.Data import Data

import unittest
import numpy as np
import matplotlib.pyplot as plt


class TestHistogram(unittest.TestCase):
    def setUp(self):
        """Set up dummy data and an instance of the Histogram class."""
        # Create synthetic data
        x_data = np.random.normal(0, 1, 1000)
        y_data = np.random.normal(5, 2, 1000)

        # Create the dataset
        self.data = Data(lat = x_data,lon = y_data)
        self.data.lat.label = 'Y Axis'
        self.data.lon.label = 'X Axis'

        # Initialize the Histogram object
        self.histogram = Histogram(data=self.data)

    def test_get_2d_range_no_custom_range(self):
        """Test the `get_2d_range` method without providing a custom range."""
        range_result, kwargs_result = self.histogram.get_2d_range('lon', 'lat')
        self.assertEqual(len(range_result), 2)
        self.assertEqual(len(range_result[0]), 2)
        self.assertEqual(len(range_result[1]), 2)
        self.assertEqual(kwargs_result, {})

    def test_get_2d_range_with_custom_range(self):
        """Test the `get_2d_range` method with a custom range."""
        custom_range = [[-3, 3], [0, 10]]
        range_result, kwargs_result = self.histogram.get_2d_range('lon', 'lat', range=custom_range)
        self.assertEqual(range_result, custom_range)
        self.assertEqual(kwargs_result, {})

    def test_plot(self):
        """Test the `plot` method for 1D histogram plotting."""
        fig, ax = plt.subplots()
        self.histogram.plot('lon', fig=fig, ax=ax, bins=20)
        self.assertEqual(self.histogram.ax.get_xlabel(), 'X Axis')
        self.assertEqual(self.histogram.ax.get_ylabel(), 'Count')

    def test_plot2d(self):
        """Test the `plot2d` method for 2D histogram plotting."""
        fig, ax = plt.subplots()
        self.histogram.plot2d('lon', 'lat', fig=fig, ax=ax, bins=(20, 20))
        self.assertEqual(self.histogram.ax.get_xlabel(), 'X Axis')
        self.assertEqual(self.histogram.ax.get_ylabel(), 'Y Axis')

    def test_plot3d(self):
        """Test the `plot3d` method for 3D surface plotting."""
        self.histogram.plot3d('lon', 'lat', bins=(20, 20))
        self.assertEqual(self.histogram.ax.get_xlabel(), 'X Axis')
        self.assertEqual(self.histogram.ax.get_ylabel(), 'Y Axis')
        self.assertEqual(self.histogram.ax.get_zlabel(), 'Count')

