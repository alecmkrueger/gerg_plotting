import unittest
from attrs import define, field
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import itertools
from pathlib import Path
import os

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
        expected_repr = """{'attr1': 10,
 'attr2': 'test'}"""
        self.assertEqual(str(self.test_instance), expected_repr)


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

        # Check the properties of the arrows matplotlib.colors.to_rgb(c)
        self.assertEqual(left_arrow.get_facecolor(),  matplotlib.colors.to_rgba(self.extent_arrows.arrow_facecolor))
        self.assertEqual(right_arrow.get_facecolor(),  matplotlib.colors.to_rgba(self.extent_arrows.arrow_facecolor))
        self.assertEqual(left_arrow.get_zorder(),  self.extent_arrows.arrow_zorder)
        self.assertEqual(right_arrow.get_zorder(),  self.extent_arrows.arrow_zorder)

    def test_add_range_arrows_facecolor_from_rectangle_facecolor(self):
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

    def test_add_range_arrows_facecolor_from_hatch(self):
        """Test arrow facecolor is derived from rectangle facecolor when set to 'coverage_color'."""
        self.extent_arrows.arrow_facecolor = 'hatch_color'
        self.extent_arrows.add_range_arrows(self.ax, self.text, self.rect)

        # Ensure arrows are added to the axes
        artists = self.ax.get_children()
        arrows = [artist for artist in artists if isinstance(artist, FancyArrow)]
        
        self.assertEqual(len(arrows), 2)
        left_arrow, right_arrow = arrows

        # Check facecolor matches rectangle facecolor
        self.assertEqual(left_arrow.get_facecolor(), self.rect.get_edgecolor())
        self.assertEqual(right_arrow.get_facecolor(), self.rect.get_edgecolor())

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

    def test_create_body_height_is_zero(self):
        coverage = Coverage()
        self.yrange = (1,1)
        coverage.create(self.xrange, self.yrange, self.label)

        # Validate body properties
        self.assertIsInstance(coverage.body, Rectangle)
        self.assertEqual(coverage.body.get_xy(), (self.xrange[0], self.yrange[0]))
        self.assertEqual(coverage.body.get_width(), self.xrange[1] - self.xrange[0])
        self.assertEqual(coverage.body.get_height(), coverage.body_min_height)

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
        background_color = "yellow"
        coverage.create(self.xrange, self.yrange, self.label,label_background_color=background_color)
        
        # Set a specific background color and test
        coverage.add_label_background(coverage.label)

        bbox = coverage.label.get_bbox_patch()
        self.assertIsNotNone(bbox)
        self.assertEqual(bbox.get_facecolor(), matplotlib.colors.to_rgba(background_color))

    def test_add_label_background_hatch(self):
        coverage = Coverage()
        body_hatch_color = 'yellow'
        background_color = "hatch_color"
        coverage.create(self.xrange, self.yrange, self.label,label_background_color=background_color,body_hatch_color=body_hatch_color)

        self.assertEqual(coverage.label_background_color,coverage.body_hatch_color)
        
        # Set a specific background color and test
        coverage.add_label_background(coverage.label)

        bbox = coverage.label.get_bbox_patch()
        self.assertIsNotNone(bbox)
        self.assertEqual(bbox.get_facecolor(),  matplotlib.colors.to_rgba(coverage.body_hatch_color))

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



class TestCoveragePlot(unittest.TestCase):

    def setUp(self):
        """Set up a basic CoveragePlot instance for testing."""
        self.fig, self.ax = plt.subplots()
        self.xlabels = ["Label1", "Label2", "Label3"]
        self.ylabels = ["LabelA", "LabelB", "LabelC"]
        self.coverage_plot = CoveragePlot(
            fig=self.fig,
            ax=self.ax,
            xlabels=self.xlabels,
            ylabels=self.ylabels,
            figsize=(10, 6),
            plotting_kwargs={"body_alpha": 0.5}
        )

    def test_post_init_cmap_str(self):
        self.fig, self.ax = plt.subplots()
        self.xlabels = ["Label1", "Label2", "Label3"]
        self.ylabels = ["LabelA", "LabelB", "LabelC"]
        self.coverage_plot = CoveragePlot(
            fig=self.fig,
            ax=self.ax,
            xlabels=self.xlabels,
            ylabels=self.ylabels,
            cmap='tab20',
            figsize=(10, 6),
            plotting_kwargs={"body_alpha": 0.5}
        )   

    def test_post_init_cmap_cmap(self):
        self.fig, self.ax = plt.subplots()
        self.xlabels = ["Label1", "Label2", "Label3"]
        self.ylabels = ["LabelA", "LabelB", "LabelC"]
        self.coverage_plot = CoveragePlot(
            fig=self.fig,
            ax=self.ax,
            xlabels=self.xlabels,
            ylabels=self.ylabels,
            cmap=plt.get_cmap('tab20'),
            figsize=(10, 6),
            plotting_kwargs={"body_alpha": 0.5}
        )   

    def test_post_init_color_iterator(self):
        """Test that the color iterator is initialized correctly."""
        self.assertIsInstance(self.coverage_plot.color_iterator, itertools.cycle)
        color = next(self.coverage_plot.color_iterator)
        self.assertTrue(isinstance(color, tuple) and len(color) == 4)  # RGBA color

    def test_post_init_grid(self):
        """Test that the grid is initialized correctly."""
        self.assertIsInstance(self.coverage_plot.grid, Grid)
        self.assertEqual(self.coverage_plot.grid.xlabels, self.xlabels)
        self.assertEqual(self.coverage_plot.grid.ylabels, self.ylabels)

    def test_coverage_color(self):
        """Test the color generation for coverages."""
        default_color = self.coverage_plot.coverage_color()
        self.coverage_plot.coverage_color_default = (0.1, 0.2, 0.3, 0.4)
        self.assertEqual(self.coverage_plot.coverage_color(), (0.1, 0.2, 0.3, 0.4))
        self.assertNotEqual(self.coverage_plot.coverage_color(), default_color)

    def test_handle_ranges_with_labels(self):
        """Test converting string labels to numeric values."""
        xrange = ["Label1", "Label2"]
        yrange = ["LabelA", "LabelB"]
        numeric_xrange, numeric_yrange = self.coverage_plot.handle_ranges(xrange, yrange)
        self.assertEqual(numeric_xrange, [0, 2])  # Adjusted for padding
        self.assertEqual(numeric_yrange, [-0.5, 1.5])  # Adjusted for padding

    def test_add_coverage(self):
        """Test adding a coverage to the plot."""
        xrange = ["Label1", "Label2"]
        yrange = ["LabelA", "LabelB"]
        self.coverage_plot.add_coverage(xrange, yrange, "Test Coverage", body_alpha=0.8)
        self.assertEqual(len(self.coverage_plot.coverages), 1)
        coverage = self.coverage_plot.coverages[0]
        self.assertIsInstance(coverage, Coverage)
        self.assertEqual(coverage.label.get_text(), "Test Coverage")

    def test_add_coverage_one_string_xrange_yrange_value(self):
        """Test adding a coverage to the plot."""
        xrange = "Label1"
        yrange = "LabelA"
        self.coverage_plot.add_coverage(xrange, yrange, "Test Coverage", body_alpha=0.8)
        self.assertEqual(len(self.coverage_plot.coverages), 1)
        coverage = self.coverage_plot.coverages[0]
        self.assertIsInstance(coverage, Coverage)
        self.assertEqual(coverage.label.get_text(), "Test Coverage")

    def test_add_coverage_missmatched_yrange_xrange(self):
        """Test adding a coverage to the plot."""
        xrange = ["Label1","Label2","Label3","Label4"]
        yrange = "LabelA"
        with self.assertRaises(ValueError):
            self.coverage_plot.add_coverage(xrange, yrange, "Test Coverage", body_alpha=0.8)

    def test_init_figure(self):
        """Test initializing a figure if none exists."""
        self.coverage_plot.fig = None
        self.coverage_plot.ax = None
        self.coverage_plot.init_figure()
        self.assertIsInstance(self.coverage_plot.fig, Figure)
        self.assertIsInstance(self.coverage_plot.ax, Axes)

    def test_custom_ticks(self):
        """Test setting custom ticks for the x-axis and y-axis."""
        self.coverage_plot.custom_ticks(labels=self.xlabels, axis='x')
        xtick_labels = [tick.get_text() for tick in self.ax.get_xticklabels()]
        self.assertEqual(xtick_labels, self.xlabels)
        self.coverage_plot.custom_ticks(labels=self.ylabels, axis='y')
        ytick_labels = [tick.get_text() for tick in self.ax.get_yticklabels()]
        self.assertEqual(ytick_labels, self.ylabels)

    def test_set_padding(self):
        """Test setting axis padding."""
        self.coverage_plot.set_padding()
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        self.assertAlmostEqual(xmin, -0.25)
        self.assertAlmostEqual(xmax, len(self.xlabels) + 0.25)
        self.assertAlmostEqual(ymin, -0.75)
        self.assertAlmostEqual(ymax, len(self.ylabels) - 1 + 0.75)

    def test_set_up_plot(self):
        """Test setting up the plot."""
        self.coverage_plot.set_up_plot(show_grid=True)
        xtick_labels = [tick.get_text() for tick in self.ax.get_xticklabels()]
        ytick_labels = [tick.get_text() for tick in self.ax.get_yticklabels()]
        self.assertEqual(xtick_labels, self.xlabels)
        self.assertEqual(ytick_labels, self.ylabels)
        self.assertTrue(self.coverage_plot.ax.get_xaxis().get_label_position(), "top")

    def test_plot_coverages(self):
        """Test plotting coverages."""
        xrange = ["Label1", "Label2"]
        yrange = ["LabelA", "LabelB"]
        self.coverage_plot.add_coverage(xrange, yrange, "Test Coverage")
        self.coverage_plot.plot_coverages()
        self.assertEqual(len(self.ax.patches), 4)  # Ensure the body, outline, left, and right arrows were added

    def test_plot(self):
        """Test plot."""
        xrange = ["Label1", "Label2"]
        yrange = ["LabelA", "LabelB"]
        self.coverage_plot.add_coverage(xrange, yrange, "Test Coverage")
        self.coverage_plot.plot()
        self.assertEqual(len(self.ax.patches), 4)  # Ensure the body, outline, left, and right arrows were added

    def test_vaild_save(self):
        """Test saving the figure."""
        output_filepath = Path("test_output.png")
        self.coverage_plot.save(output_filepath)
        self.assertTrue(output_filepath.exists())
        if output_filepath.exists():
            os.remove("test_output.png")

    def test_invaid_save(self):
        """Test saving an invalid figure."""
        self.coverage_plot.fig = None
        with self.assertRaises(ValueError):
            self.coverage_plot.save('test_output.png')


    def test_show(self):
        self.coverage_plot.show(block=False)
        plt.close('all')

