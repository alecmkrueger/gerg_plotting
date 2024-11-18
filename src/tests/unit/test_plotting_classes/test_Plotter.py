from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.tools import data_from_csv

import unittest
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class TestPlotter(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment for Plotter with basic data.
        """
        self.data = {
            "x": np.linspace(0, 10, 100),
            "y": np.sin(np.linspace(0, 10, 100)),
        }
        self.plotter = Plotter()

    def test_create_figure(self):
        """
        Test that create_figure initializes a matplotlib figure with correct attributes.
        """
        fig, ax = self.plotter.create_figure()
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

    def test_scatter_plot(self):
        """
        Test that a scatter plot is created and data is plotted correctly.
        """
        fig, ax = self.plotter.create_figure()
        self.plotter.scatter(ax=ax, x=self.data["x"], y=self.data["y"])
        scatter_points = ax.collections[0]  # Scatter plot data is stored in `collections`
        self.assertEqual(len(scatter_points.get_offsets()), len(self.data["x"]))

