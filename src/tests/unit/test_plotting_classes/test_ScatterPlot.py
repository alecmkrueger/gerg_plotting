import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from gerg_plotting.data_classes.Data import Data
from gerg_plotting.data_classes.Variable import Variable
from gerg_plotting.plotting_classes.ScatterPlot import ScatterPlot


class TestScatterPlot(unittest.TestCase):
    def setUp(self):
        """
        Create test data and initialize a ScatterPlot instance for testing.
        """
        # Generate synthetic data
        # time = np.arange(10)
        time = pd.date_range('2024-07-10',periods=10)
        depth = np.linspace(0, 100, 10)
        salinity = np.random.uniform(30, 35, 10)
        temperature = np.random.uniform(10, 20, 10)
        u = np.random.uniform(-1, 1, 10)
        v = np.random.uniform(-1, 1, 10)

        # Create Variable objects
        self.data = {
            "time": Variable(time, name="time", units="s", label="Time"),
            "depth": Variable(depth, name="depth", units="m", label="Depth"),
            "salinity": Variable(salinity, name="salinity", units="PSU", label="Salinity"),
            "temperature": Variable(temperature, name="temperature", units="°C", label="Temperature"),
            "u": Variable(u, name="u", units="m/s", label="Zonal Velocity"),
            "v": Variable(v, name="v", units="m/s", label="Meridional Velocity"),
        }

        self.data = Data(**self.data)

        # Initialize ScatterPlot
        self.plotter = ScatterPlot(data=self.data)

    def test_get_density_color_data(self):
        self.plotter.get_density_color_data(color_var='density')

    def test_scatter(self):
        """
        Test the scatter plot method for valid execution.
        """
        fig, ax = plt.subplots()
        scatter = self.plotter.scatter(x="salinity", y="temperature", color_var="depth", fig=fig, ax=ax)
        
        # Assert that the scatter plot is created
        self.assertIsNotNone(scatter)
        plt.close(fig)

    def test_scatter_time(self):
        """
        Test the scatter plot method for valid execution.
        """
        fig, ax = plt.subplots()
        scatter = self.plotter.scatter(x="salinity", y="temperature", color_var="time", fig=fig, ax=ax)
        
        # Assert that the scatter plot is created
        self.assertIsNotNone(scatter)
        plt.close(fig)

    def test_scatter_no_var(self):
        """
        Test the scatter plot method for valid execution.
        """
        fig, ax = plt.subplots()
        scatter = self.plotter.scatter(x="salinity", y="temperature", fig=fig, ax=ax)
        
        # Assert that the scatter plot is created
        self.assertIsNotNone(scatter)
        plt.close(fig)

    def test_hovmoller(self):
        """
        Test the hovmoller method for depth vs. time plotting.
        """
        fig, ax = plt.subplots()
        self.plotter.hovmoller(var="salinity", fig=fig, ax=ax)

        # Assert the axes are formatted correctly
        self.assertEqual(ax.get_xlabel(), "Time")
        self.assertEqual(ax.get_ylabel(), "Depth")
        plt.close(fig)

    def test_TS(self):
        """
        Test the T-S plot with optional sigma-theta contours.
        """
        fig, ax = plt.subplots()
        self.plotter.TS(color_var="depth", fig=fig, ax=ax, contours=True)

        # Assert the title and axes labels
        self.assertEqual(ax.get_title(), "T-S Diagram")
        self.assertEqual(ax.get_xlabel(), "Salinity")
        self.assertEqual(ax.get_ylabel(), "Temperature")
        plt.close(fig)

    def test_quiver1d(self):
        """
        Test the 1D quiver plot method for velocity vectors.
        """
        fig, ax = plt.subplots()
        self.plotter.quiver1d(x="time", quiver_density=5, quiver_scale=1, fig=fig, ax=ax)

        # Assert that y-axis is hidden
        self.assertFalse(ax.yaxis.get_visible())
        plt.close(fig)

    def test_quiver2d(self):
        """
        Test the 2D quiver plot method for velocity vectors.
        """
        fig, ax = plt.subplots()
        self.plotter.quiver2d(x="time", y="depth", quiver_density=2, quiver_scale=1, fig=fig, ax=ax)

        # Assert the axes labels
        self.assertEqual(ax.get_xlabel(), "Time")
        self.assertEqual(ax.get_ylabel(), "Depth")
        plt.close(fig)

    def test_power_spectra_density(self):
        """
        Test the PSD plotting method with generated data.
        """
        psd_freq = np.logspace(-2, 1, 10)  # Example frequencies
        psd = np.random.uniform(1, 10, 10)  # Example PSD values

        # Add PSD variables to data
        psd_freq = Variable(psd_freq, name="psd_freq", units="Hz", label="Frequency (Hz)")
        psd_example = Variable(psd, name="psd_example", units="dB", label="Power Spectra Density")
        # self.data.add_custom_variable(psd_freq)
        # self.data.add_custom_variable(psd_example)

        fig, ax = plt.subplots()
        self.plotter.power_spectra_density(psd_freq=psd_freq, psd=psd_example, var_name="example", fig=fig, ax=ax)

        # Assert that the plot is created
        self.assertEqual(ax.get_xlabel(), "Frequency (Hz)")
        self.assertEqual(ax.get_ylabel(), "Power Spectra Density")
        plt.close(fig)

