import unittest
from attrs import define, field
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.text import Text
from matplotlib.axes import Axes

from gerg_plotting.plotting_classes.CoveragePlot import Base,Grid,ExtentArrows,Coverage,CoveragePlot

class TestBase(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of the Base class."""
        @define
        class TestClass(Base):
            attr1: int = field(default=10)
            attr2: str = field(default="test")

        self.test_instance = TestClass()

    def test_has_var_true(self):
        """Test _has_var method returns True for existing attributes."""
        self.assertTrue(self.test_instance._has_var("attr1"))
        self.assertTrue(self.test_instance._has_var("attr2"))

    def test_has_var_false(self):
        """Test _has_var method returns False for non-existent attributes."""
        self.assertFalse(self.test_instance._has_var("non_existent"))

    def test_get_vars(self):
        """Test get_vars method returns the list of attributes."""
        self.assertEqual(self.test_instance.get_vars(), ["attr1", "attr2"])

    def test_getitem_existing_key(self):
        """Test __getitem__ method for existing keys."""
        self.assertEqual(self.test_instance["attr1"], 10)
        self.assertEqual(self.test_instance["attr2"], "test")

    def test_getitem_non_existent_key(self):
        """Test __getitem__ raises KeyError for non-existent keys."""
        with self.assertRaises(KeyError):
            _ = self.test_instance["non_existent"]

    def test_setitem_existing_key(self):
        """Test __setitem__ updates existing attributes."""
        self.test_instance["attr1"] = 20
        self.assertEqual(self.test_instance.attr1, 20)

    def test_setitem_non_existent_key(self):
        """Test __setitem__ raises KeyError for non-existent attributes."""
        with self.assertRaises(KeyError):
            self.test_instance["non_existent"] = "value"

    def test_repr(self):
        """Test __repr__ returns a pretty-printed string representation."""
        expected_repr = """{
 'attr1': 10,
 'attr2': 'test'
}"""
        self.assertEqual(repr(self.test_instance), expected_repr)


class TestGrid(unittest.TestCase):
    def setUp(self):
        """Set up a matplotlib Axes object and a Grid instance for testing."""
        self.fig, self.ax = plt.subplots()
        self.xlabels = ["A", "B", "C"]
        self.ylabels = ["1", "2", "3"]
        self.grid = Grid(xlabels=self.xlabels, ylabels=self.ylabels)

    def test_add_hlines(self):
        """Test that horizontal lines are added to the axes at correct positions."""
        y_values = [0.5, 1.5, 2.5]
        self.grid.add_hlines(ax=self.ax, y_values=y_values, color="red", linewidth=2)

        hlines = [line for line in self.ax.get_lines() if line.get_linestyle() == "-"]
        self.assertEqual(len(hlines), len(y_values))

        for line, y in zip(hlines, y_values):
            self.assertEqual(line.get_ydata()[0], y)
            self.assertEqual(line.get_ydata()[1], y)
            self.assertEqual(line.get_color(), "red")
            self.assertEqual(line.get_linewidth(), 2)

    def test_add_vlines(self):
        """Test that vertical lines are added to the axes at correct positions."""
        x_values = [0.5, 1.5, 2.5]
        self.grid.add_vlines(ax=self.ax, x_values=x_values, color="blue", linestyle="-.", linewidth=1)

        vlines = [line for line in self.ax.get_lines() if line.get_linestyle() == "-."]
        self.assertEqual(len(vlines), len(x_values))

        for line, x in zip(vlines, x_values):
            self.assertEqual(line.get_xdata()[0], x)
            self.assertEqual(line.get_xdata()[1], x)
            self.assertEqual(line.get_color(), "blue")
            self.assertEqual(line.get_linewidth(), 1)

    def test_add_grid(self):
        """Test that a complete grid is added with the correct properties."""
        self.grid.add_grid(self.ax, grid_linewidth=1.5, grid_color="green", grid_linestyle=":")

        hlines = [line for line in self.ax.get_lines() if line.get_xdata()[0] == line.get_xdata()[1]]
        vlines = [line for line in self.ax.get_lines() if line.get_ydata()[0] == line.get_ydata()[1]]

        self.assertEqual(len(hlines), len(self.ylabels) + 1)  # Include borders
        self.assertEqual(len(vlines), len(self.xlabels) + 1)  # Include borders

        for line in hlines + vlines:
            self.assertEqual(line.get_linewidth(), 1.5)
            self.assertEqual(line.get_color(), "green")
            self.assertEqual(line.get_linestyle(), ":")


class TestExtentArrows(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of ExtentArrows and a Matplotlib Axes."""
        self.fig, self.ax = plt.subplots()
        self.extent_arrows = ExtentArrows()
        
        # Add a rectangle and text for testing
        self.rect = Rectangle((0.2, 0.4), 0.3, 0.2, facecolor='blue', edgecolor='red')
        self.text = Text(x=0.5, y=0.6, text='Test')
        self.ax.add_patch(self.rect)
        self.ax.add_artist(self.text)

    def test_calculate_arrow_length(self):
        """Test calculation of arrow lengths based on rectangle and text positions."""
        left_arrow_length, right_arrow_length = self.extent_arrows.calculate_arrow_length(
            self.ax, self.rect, self.text.get_position()[0] - 0.1, self.text.get_position()[0] + 0.1
        )

        self.assertAlmostEqual(left_arrow_length, 0.2 - (self.text.get_position()[0] - 0.1), delta=0.1)
        self.assertAlmostEqual(right_arrow_length, (0.2 + 0.3) - (self.text.get_position()[0] + 0.1), delta=0.1)

    def test_add_range_arrows_default_properties(self):
        """Test adding range arrows with default properties."""
        self.extent_arrows.add_range_arrows(self.ax, self.text, self.rect)

        # Ensure arrows are added to the axes
        artists = self.ax.get_children()
        arrows = [artist for artist in artists if isinstance(artist, FancyArrow)]
        
        self.assertEqual(len(arrows), 2)
        left_arrow, right_arrow = arrows

        # Check the properties of the arrows
        self.assertEqual(left_arrow.get_facecolor(), self.extent_arrows.arrow_facecolor)
        self.assertEqual(right_arrow.get_facecolor(), self.extent_arrows.arrow_facecolor)
        self.assertEqual(left_arrow.get_zorder(), self.extent_arrows.arrow_zorder)
        self.assertEqual(right_arrow.get_zorder(), self.extent_arrows.arrow_zorder)

    def test_add_range_arrows_facecolor_from_rectangle(self):
        """Test arrow facecolor is derived from rectangle facecolor when set to 'coverage_color'."""
        self.extent_arrows.arrow_facecolor = 'coverage_color'
        self.extent_arrows.add_range_arrows(self.ax, self.text, self.rect)

        # Ensure arrows are added to the axes
        artists = self.ax.get_children()
        arrows = [artist for artist in artists if isinstance(artist, FancyArrow)]
        
        self.assertEqual(len(arrows), 2)
        left_arrow, right_arrow = arrows

        # Check facecolor matches rectangle facecolor
        self.assertEqual(left_arrow.get_facecolor(), self.rect.get_facecolor())
        self.assertEqual(right_arrow.get_facecolor(), self.rect.get_facecolor())

    def tearDown(self):
        """Close the plot after each test to avoid resource leaks."""
        plt.close(self.fig)


class TestCoverage(unittest.TestCase):

    def setUp(self):
        self.fig, self.ax = plt.subplots()
        self.xrange = (0, 5)
        self.yrange = (0, 3)
        self.label = "Test Label"
        
    def test_create_body(self):
        coverage = Coverage()
        coverage.create(self.xrange, self.yrange, self.label)

        # Validate body properties
        self.assertIsInstance(coverage.body, Rectangle)
        self.assertEqual(coverage.body.get_xy(), (self.xrange[0], self.yrange[0]))
        self.assertEqual(coverage.body.get_width(), self.xrange[1] - self.xrange[0])
        self.assertEqual(coverage.body.get_height(), self.yrange[1] - self.yrange[0])

    def test_create_outline(self):
        coverage = Coverage()
        coverage.create(self.xrange, self.yrange, self.label)

        # Validate outline properties
        self.assertIsInstance(coverage.outline, Rectangle)
        self.assertEqual(coverage.outline.get_xy(), (self.xrange[0], self.yrange[0]))
        self.assertEqual(coverage.outline.get_width(), self.xrange[1] - self.xrange[0])
        self.assertEqual(coverage.outline.get_height(), self.yrange[1] - self.yrange[0])
        self.assertFalse(coverage.outline.get_fill())

    def test_create_label(self):
        coverage = Coverage()
        coverage.create(self.xrange, self.yrange, self.label)

        # Validate label properties
        self.assertIsInstance(coverage.label, Text)
        self.assertEqual(coverage.label.get_text(), self.label)
        self.assertAlmostEqual(coverage.label.get_position()[0], sum(self.xrange) / 2)
        self.assertAlmostEqual(coverage.label.get_position()[1], sum(self.yrange) / 2)

    def test_add_label_background(self):
        coverage = Coverage()
        coverage.create(self.xrange, self.yrange, self.label)
        
        # Set a specific background color and test
        background_color = "yellow"
        coverage.add_label_background(coverage.label, background_color)

        bbox = coverage.label.get_bbox_patch()
        self.assertIsNotNone(bbox)
        self.assertEqual(bbox.get_facecolor(), plt.colors.to_rgba(background_color))

    def test_create_with_extent_arrows(self):
        coverage = Coverage()
        kwargs = {"arrow_facecolor": "red", "arrow_edgecolor": "blue"}
        coverage.create(self.xrange, self.yrange, self.label, **kwargs)

        # Validate extent arrows
        self.assertIsInstance(coverage.extent_arrows, ExtentArrows)
        self.assertEqual(coverage.extent_arrows.arrow_facecolor, "red")
        self.assertEqual(coverage.extent_arrows.arrow_edgecolor, "blue")

    def test_plot(self):
        coverage = Coverage()
        coverage.create(self.xrange, self.yrange, self.label)
        coverage.plot(self.ax)

        # Validate that the elements were added to the axes
        self.assertIn(coverage.body, self.ax.patches)
        self.assertIn(coverage.outline, self.ax.patches)
        self.assertIn(coverage.label, self.ax.texts)

