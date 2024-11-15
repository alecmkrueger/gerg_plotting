from gerg_plotting.modules.plotting import colorbar,get_turner_cmap

import unittest
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

class TestColorbarFunction(unittest.TestCase):
    def setUp(self):
        # Create a test figure and axes
        self.fig, self.ax = plt.subplots()
        self.divider = make_axes_locatable(self.ax)
        self.test_data = np.random.rand(10, 10)
        self.mappable = self.ax.imshow(self.test_data)
        self.label = "Test Label"

    def test_colorbar_added(self):
        """Test that a colorbar is added to the figure."""
        initial_axes_count = len(self.fig.axes)
        colorbar(self.fig, self.divider, self.mappable, self.label)
        self.assertEqual(len(self.fig.axes), initial_axes_count + 1, "Colorbar axes were not added.")

    def test_colorbar_label(self):
        """Test that the colorbar has the correct label."""
        cbar = colorbar(self.fig, self.divider, self.mappable, self.label)
        self.assertEqual(cbar.ax.get_ylabel(), self.label, "Colorbar label does not match the expected value.")

    def tearDown(self):
        plt.close(self.fig)


class TestGetTurnerCmapFunction(unittest.TestCase):
    def test_cmap_type(self):
        """Test that the returned object is a ListedColormap."""
        cmap = get_turner_cmap()
        self.assertIsInstance(cmap, ListedColormap, "The returned object is not a ListedColormap.")

    def test_cmap_color_count(self):
        """Test that the colormap contains the expected number of colors."""
        cmap = get_turner_cmap()
        self.assertEqual(cmap.N, 256, "The colormap does not have 256 colors.")

    def test_cmap_color_ranges(self):
        """Test that the color ranges are modified as expected."""
        cmap = get_turner_cmap()
        colors = cmap(np.linspace(0, 1, 256))

        # Check first 12.5% of colors (red)
        self.assertTrue(np.allclose(colors[:32], [1, 0, 0, 1]), "First color range is incorrect (red).")

        # Check next 25% of colors (yellow)
        self.assertTrue(np.allclose(colors[32:96], [1, 1, 0, 1]), "Second color range is incorrect (yellow).")

        # Check next 25% of colors (green)
        self.assertTrue(np.allclose(colors[96:160], [0, 1, 0, 1]), "Third color range is incorrect (green).")

        # Check next 25% of colors (blue)
        self.assertTrue(np.allclose(colors[160:224], [0, 0, 1, 1]), "Fourth color range is incorrect (blue).")

        # Check last 12.5% of colors (red)
        self.assertTrue(np.allclose(colors[224:], [1, 0, 0, 1]), "Last color range is incorrect (red).")

