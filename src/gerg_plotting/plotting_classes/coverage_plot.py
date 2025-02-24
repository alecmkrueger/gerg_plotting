# CoveragePlot.py

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
from matplotlib.ticker import FixedLocator
from matplotlib.text import Text
from matplotlib.patches import Rectangle,FancyArrow
from attrs import define,field,asdict
from pprint import pformat
import itertools

from gerg_plotting.modules.utilities import extract_kwargs_with_aliases
from gerg_plotting.modules.base_config import BaseConfig
from gerg_plotting.tools.tools import normalize_string,merge_dicts

@define
class GridConfig(BaseConfig):
    """Configuration for grid styling."""
    
    grid_linewidth: float = 1
    """Width of grid lines."""
    
    grid_linestyle: str = '--'
    """Style of grid lines."""
    
    grid_color: str|tuple = 'black'
    """Color of grid lines."""
    
    grid_zorder: float = 1.15
    """Z-order of grid lines."""

@define
class ExtentArrowConfig(BaseConfig):
    """Configuration for extent arrows."""
    
    arrow_facecolor: str|tuple = 'black'
    """Color of arrow fill"""
    
    arrow_edgecolor: str|tuple = 'black'
    """Color of arrow edges."""
    
    arrow_tail_width: float = 0.05
    """Width of arrow tail."""
    
    arrow_head_width: float = 0.12
    """Width of arrow head."""
    
    arrow_zorder: float = 2.9
    """Z-order for arrow drawing."""
    
    arrow_linewidth: float = 0
    """Width of arrow lines."""
    
    arrow_text_padding: float = 0.05
    """Padding between arrow and text."""

@define
class CoverageConfig(BaseConfig):
    """Configuration for coverage styling."""
    
    body_min_height: float = 0.25
    """Minimum height for coverage body."""
    
    body_alpha: float = 1
    """Transparency of coverage body."""
    
    body_linewidth: float = 1
    """Line width of coverage body."""
    
    body_color: str|tuple = 'none'
    """Fill color of coverage body."""
    
    body_hatch: str = None
    """Hatch pattern for coverage body."""
    
    body_hatch_color: str = None
    """Color of hatch pattern."""

    body_outline_alpha: float = 1
    """Transparency of body outline."""
    
    hatch_linewidth: float = 0.5
    """Width of hatch lines."""
    
    outline_edgecolor: str|tuple = 'k'
    """Color of outline."""
    
    outline_alpha: float = 1
    """Transparency of outline."""
    
    outline_linewidth: float = 1
    """Width of outline."""
    
    label_fontsize: float = 12
    """Font size for label."""

    label_font_color: str|tuple = 'black'
    """Color of label font."""
    
    label_background_pad: float = 2
    """Padding around label background."""
    
    label_background_linewidth: float = 0
    """Width of label background border."""
    
    label_background_alpha: float = 1
    """Transparency of label background."""

    label_position: tuple = None
    """Position of label in (x, y) format and in the units of the plot."""

    show_arrows: bool = True
    """Whether to show extent arrows."""

    _label_background_color: str|tuple = 'body_color'
    """Color of label background."""

    @property
    def label_background_color(self):
        """Get the label background color."""
        if self._label_background_color == 'body_color':
            return self.body_color
        return self._label_background_color
    
    @label_background_color.setter
    def label_background_color(self, value):
        """Set the label background color."""
        self._label_background_color = value


@define
class CoveragePlotConfig(BaseConfig):
    """Main configuration class for coverage plotting."""
    
    # Overall plot settings
    horizontal_padding: float = 0.25
    vertical_padding: float = 0.75
    coverage_color_default: str|tuple = None
    
    # Sub-configurations
    grid: GridConfig = field(factory=GridConfig)
    arrow: ExtentArrowConfig = field(factory=ExtentArrowConfig)
    coverage: CoverageConfig = field(factory=CoverageConfig)
    
    def update(self, config_dict):
        """Update config values from a flat dictionary by routing to appropriate sub-configs."""
        for k, v in config_dict.items():
            # Direct attributes of this class
            if hasattr(self, k) and k not in ['grid', 'arrow', 'coverage']:
                setattr(self, k, v)
            # Grid config attributes
            elif hasattr(self.grid, k):
                setattr(self.grid, k, v)
            # Arrow config attributes
            elif hasattr(self.arrow, k):
                setattr(self.arrow, k, v)
            # Coverage config attributes
            elif hasattr(self.coverage, k):
                setattr(self.coverage, k, v)
            # Unknown attribute
            else:
                raise AttributeError(f"No configuration setting found for: {k}")
        return self


@define
class Base:
    """
    Base class providing common functionality for attribute access and variable management.

    Methods
    -------
    _has_var(key)
        Check if object has a specific variable.
    get_vars()
        Get list of all object variables/attributes.
    __getitem__(key)
        Enable dictionary-style access to class attributes.
    __setitem__(key, value)
        Enable dictionary-style setting of class attributes.
    __str__()
        Return formatted string representation of class attributes.
    """
    def _has_var(self, key) -> bool:
        """
        Base class providing common functionality for attribute access and variable management.

        Methods
        -------
        _has_var(key)
            Check if object has a specific variable.
        get_vars()
            Get list of all object variables/attributes.
        __getitem__(key)
            Enable dictionary-style access to class attributes.
        __setitem__(key, value)
            Enable dictionary-style setting of class attributes.
        __str__()
            Return formatted string representation of class attributes.
        """
        return key in asdict(self).keys()
    
    def get_vars(self) -> list:
        """
        Get list of all object variables/attributes.

        Returns
        -------
        list
            List of all variable names in the object.
        """
        return list(asdict(self).keys())

    def __getitem__(self, key: str):
        """
        Enable dictionary-style access to class attributes.

        Parameters
        ----------
        key : str
            The name of the attribute to access.

        Returns
        -------
        Any
            The value of the specified attribute.

        Raises
        ------
        KeyError
            If the specified attribute doesn't exist.
        """
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")  

    def __setitem__(self, key, value) -> None:
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")

    def __str__(self) -> None:
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)



@define
class Grid(Base):
    """A class for managing and drawing grid lines on a plot."""
    xlabels: list
    ylabels: list
    config: GridConfig = field(factory=GridConfig)
    
    def add_hlines(self, ax: Axes, y_values):
        """Add horizontal lines to the plot using config settings."""
        for y_value in y_values:
            ax.axhline(
                y_value, 
                zorder=self.config.grid_zorder,
                linewidth=self.config.grid_linewidth,
                linestyle=self.config.grid_linestyle,
                color=self.config.grid_color
            )

    def add_vlines(self, ax: Axes, x_values):
        """Add vertical lines to the plot using config settings."""
        for x_value in x_values:
            ax.axvline(
                x_value, 
                zorder=self.config.grid_zorder,
                linewidth=self.config.grid_linewidth,
                linestyle=self.config.grid_linestyle,
                color=self.config.grid_color
            )

    def add_grid(self, ax):
        """Add complete grid to the plot with both horizontal and vertical lines."""
        n_hlines = len(self.ylabels)
        n_vlines = len(self.xlabels)
        self.add_hlines(ax=ax, y_values=np.arange(-0.5, n_hlines+0.5, 1))
        self.add_vlines(ax=ax, x_values=np.arange(0, n_vlines+1, 1))

@define
class ExtentArrows(Base):
    """A class for managing and drawing arrows that indicate coverage extents."""
    label_position: tuple = field(default=None)
    left_arrow: FancyArrow = field(default=None)
    right_arrow: FancyArrow = field(default=None)
    top_arrow: FancyArrow = field(default=None)
    bottom_arrow: FancyArrow = field(default=None)
    config: ExtentArrowConfig = field(factory=ExtentArrowConfig)
    
    def calculate_arrow_length(self, ax: Axes, rect, text_left, text_right):
        """Calculate the lengths needed for extent arrows."""
        rect_bbox = ax.transData.inverted().transform(rect.get_window_extent())
        rect_left, rect_bottom = rect_bbox[0]
        rect_right, rect_top = rect_bbox[1]
        left_arrow_length = rect_left-text_left
        right_arrow_length = rect_right-text_right
        return left_arrow_length, right_arrow_length

    def add_range_arrows(self, ax: Axes, text: Text, rect: Rectangle):
        """Add arrows indicating the range of coverage using config settings."""
        if self.config.arrow_facecolor == 'coverage_color':
            arrow_facecolor = rect.get_facecolor()
        elif self.config.arrow_facecolor == 'hatch_color':
            arrow_facecolor = rect.get_edgecolor()
        else:
            arrow_facecolor = self.config.arrow_facecolor

        text_bbox = ax.transData.inverted().transform(text.get_window_extent())
        text_left, text_bottom = text_bbox[0]
        text_right, text_top = text_bbox[1]
        text_y_center = (text_bottom + text_top) / 2

        arrow_props = {
            'width': self.config.arrow_tail_width,
            'facecolor': arrow_facecolor,
            'head_width': self.config.arrow_head_width,
            'length_includes_head': True,
            'zorder': self.config.arrow_zorder,
            'edgecolor': self.config.arrow_edgecolor,
            'linewidth': self.config.arrow_linewidth
        }

        left_arrow_length, right_arrow_length = self.calculate_arrow_length(
            ax, rect, text_left=text_left, text_right=text_right
        )

        left_arrow_left_bound = text_left - self.config.arrow_text_padding
        left_arrow_right_bound = left_arrow_length + self.config.arrow_text_padding

        right_arrow_left_bound = text_right + self.config.arrow_text_padding
        right_arrow_right_bound = right_arrow_length - self.config.arrow_text_padding

        left_arrow = FancyArrow(left_arrow_left_bound, text_y_center, left_arrow_right_bound, 0, **arrow_props)
        right_arrow = FancyArrow(right_arrow_left_bound, text_y_center, right_arrow_right_bound, 0, **arrow_props)

        ax.add_artist(left_arrow)
        ax.add_artist(right_arrow)


@define
class Coverage(Base):
    """A class for creating and managing plots showing multiple coverage areas."""
    body: Rectangle = field(init=False)
    outline: Rectangle = field(init=False)
    label: Text = field(init=False)
    extent_arrows: ExtentArrows = field(factory=ExtentArrows)
    anchor_point: tuple[float, float] = field(init=False)
    width: float = field(init=False)
    height: float = field(init=False)
    config: CoverageConfig = field(factory=CoverageConfig)
    
    def create(self, xrange, yrange, label):
        """Create a new coverage object with specified range and label."""
        self._calculate_dimensions(xrange, yrange)
        self._create_body()
        self._create_outline()
        self._create_label(label)
        self._create_arrows()
        return self

    def _calculate_dimensions(self, xrange, yrange):
        """Calculate coverage dimensions."""
        self.anchor_point = (xrange[0], yrange[0])
        self.width = xrange[1] - xrange[0]
        self.height = max(yrange[1] - yrange[0], self.config.body_min_height)

    def _create_body(self):
        """Create the coverage body rectangle."""
        matplotlib.rcParams['hatch.linewidth'] = self.config.hatch_linewidth
        self.body = Rectangle(
            self.anchor_point, width=self.width, height=self.height,
            fc=self.config.body_color, alpha=self.config.body_alpha,
            linewidth=self.config.body_linewidth, edgecolor=self.config.body_hatch_color,
            hatch=self.config.body_hatch
        )

    def _create_outline(self):
        """Create the coverage outline rectangle."""
        self.outline = Rectangle(
            self.anchor_point, width=self.width, height=self.height,
            fc=None, fill=False, alpha=self.config.outline_alpha,
            linewidth=self.config.outline_linewidth, edgecolor=self.config.outline_edgecolor,
            zorder=self.body.get_zorder()+0.1
        )

    def _create_label(self, label):
        """Create the coverage label."""
        position = self.config.label_position
        if position is None:
            position = self.body.get_center()
        self.label = Text(
            *position, text=label,
            fontsize=self.config.label_fontsize,
            color=self.config.label_font_color,
            ha='center', va='center', zorder=5
        )

    def _create_arrows(self):
        """Create extent arrows if enabled."""
        if self.config.show_arrows:
            self.extent_arrows = ExtentArrows()
            # No need to manually transfer config settings - handled by CoveragePlot

    def _add_label_background(self, text: Text):
        """Add background to coverage label."""
        text.set_bbox(dict(
            facecolor=self.config.label_background_color,
            pad=self.config.label_background_pad,
            linewidth=self.config.label_background_linewidth,
            alpha=self.config.label_background_alpha
        ))

    def plot(self, ax: Axes):
        """Plot the coverage on given axes using config settings."""
        ax.add_artist(self.body)
        ax.add_artist(self.outline)
        ax.add_artist(self.label)
        self._add_label_background(self.label)
        if self.config.show_arrows:
            self.extent_arrows.add_range_arrows(ax=ax, text=self.label, rect=self.body)

@define
class CoveragePlot(Base):
    """
    A class for creating and managing plots showing multiple coverage areas.
    """
    fig: Figure = field(default=None)
    ax: Axes = field(default=None)
    figsize: tuple = field(default=None)
    xlabels: list = field(default=None)
    ylabels: list = field(default=None)
    cmap: str|Colormap = field(default=None)
    color_iterator: itertools.cycle = field(init=False)
    coverages: list[Coverage] = field(factory=list)
    grid: Grid = field(init=False)

    # Single unified config object
    config: CoveragePlotConfig = field(factory=CoveragePlotConfig)
    
    def __attrs_post_init__(self):
        """
        Initializes the ColorCycler and the coverages container
        """
        if self.cmap is None:
            self.cmap = plt.get_cmap('tab10')
        elif isinstance(self.cmap, str):
            self.cmap = plt.get_cmap(self.cmap)
        
        n_colors = self.cmap.N
        self.color_iterator = itertools.cycle(
            (self.cmap(i / (n_colors - 1)) for i in range(n_colors))
        )

        # Initialize grid with its config from the hierarchical config
        self.grid = Grid(xlabels=self.xlabels, ylabels=self.ylabels)
        self.grid.config = self.config.grid

    def update_config(self, **kwargs):
        """
        Update configuration settings across all components.
        
        Parameters
        ----------
        **kwargs
            Configuration settings to update
        """
        # Update the main config which will route to appropriate sub-configs
        self.config.update(kwargs)
        
        # Apply sub-configs to existing coverages
        for coverage in self.coverages:
            coverage.config = self.config.coverage
            if coverage.extent_arrows:
                coverage.extent_arrows.config = self.config.arrow
                
        # Update grid config
        self.grid.config = self.config.grid
        
        return self

    def _extract_config_kwargs(self, kwargs: dict) -> tuple[dict, dict]:
        """
        Extract configuration kwargs from general kwargs.
        
        Parameters
        ----------
        kwargs : dict
            Mixed kwargs containing both config and non-config parameters
            
        Returns
        -------
        tuple[dict, dict]
            (config_kwargs, remaining_kwargs)
        """
        # Collect all possible config attributes
        config_attrs = set()
        config_attrs.update(CoverageConfig().to_dict().keys())
        config_attrs.update(ExtentArrowConfig().to_dict().keys())
        config_attrs.update(GridConfig().to_dict().keys())
        
        # Separate kwargs
        config_kwargs = {k: v for k, v in kwargs.items() if k in config_attrs}
        remaining_kwargs = {k: v for k, v in kwargs.items() if k not in config_attrs}
        return config_kwargs, remaining_kwargs
    
    def set_default_config(self, value: dict | CoveragePlotConfig):
        """
        Set new default configuration for all future coverages.
        
        Parameters
        ----------
        value : dict or CoveragePlotConfig
            New default configuration values
        """
        if isinstance(value, dict):
            # Handle CoverageConfig attributes
            coverage_attrs = {k: v for k, v in value.items() 
                           if hasattr(CoverageConfig(), k)}
            if coverage_attrs:
                for coverage in self.coverages:
                    coverage.config = coverage_attrs

            # Handle GridConfig attributes
            grid_attrs = {k: v for k, v in value.items() 
                        if hasattr(GridConfig(), k)}
            if grid_attrs:
                self.grid.config = grid_attrs

            # Handle ExtentArrowConfig attributes
            arrow_attrs = {k: v for k, v in value.items()
                         if hasattr(ExtentArrowConfig(), k)}
            if arrow_attrs:
                for coverage in self.coverages:
                    if coverage.extent_arrows:
                        coverage.extent_arrows.config = arrow_attrs

            # Handle CoveragePlotConfig attributes
            plot_attrs = {k: v for k, v in value.items() 
                        if hasattr(CoveragePlotConfig(), k)}
            if plot_attrs:
                self._default_config = CoveragePlotConfig(**plot_attrs)
                self._config = self._default_config
        else:
            self._default_config = value
            self._config = value

    def add_coverage(self, xrange, yrange, label=None, **config_override):
        """Add a new coverage area with optional custom configuration."""
        xrange = [xrange] if not isinstance(xrange, list) else xrange
        yrange = [yrange] if not isinstance(yrange, list) else yrange

        # Extend single values to ranges
        if len(xrange) == 1:
            xrange.extend(xrange)
        if len(yrange) == 1:
            yrange.extend(yrange)

        if len(xrange) == len(yrange):
            # Convert string labels to numeric indices
            xrange, yrange = self.handle_ranges(xrange=xrange, yrange=yrange)
            
            # Create new coverage with default config from the hierarchical config
            coverage = Coverage()
            coverage.config = self.config.coverage
            
            # Apply local config overrides if any
            if config_override:
                # Create a copy of coverage config and update it
                local_coverage_config = CoverageConfig()
                local_coverage_config.update(config_override)
                
                # Filter config_override for coverage config keys
                coverage_keys = set(local_coverage_config.to_dict().keys())
                coverage_overrides = {k: v for k, v in config_override.items() 
                                     if k in coverage_keys}
                
                # Apply overrides
                for k, v in coverage_overrides.items():
                    setattr(local_coverage_config, k, v)
                
                coverage.config = local_coverage_config
            
            coverage = coverage.create(xrange=xrange, yrange=yrange, label=label)
            
            # Configure extent arrows with arrow config
            if coverage.extent_arrows:
                if config_override:
                    # Similar to coverage, apply any arrow-specific overrides
                    arrow_keys = set(self.config.arrow.to_dict().keys())
                    arrow_overrides = {k: v for k, v in config_override.items()
                                     if k in arrow_keys}
                    
                    if arrow_overrides:
                        local_arrow_config = ExtentArrowConfig(**self.config.arrow.to_dict())
                        for k, v in arrow_overrides.items():
                            setattr(local_arrow_config, k, v)
                        coverage.extent_arrows.config = local_arrow_config
                    else:
                        coverage.extent_arrows.config = self.config.arrow
                else:
                    coverage.extent_arrows.config = self.config.arrow
                    
            self.coverages.append(coverage)
            return


    def save(self,filename,**kwargs):
        """
        Save the current figure to a file.

        Parameters
        ----------
        filename : str
            Path to save the figure.
        ``**kwargs``
            Additional keyword arguments passed to savefig.

        Raises
        ------
        ValueError
            If no figure exists to save.
        """
        if self.fig is not None:
            self.fig.savefig(fname=filename,**kwargs)
        else:
            raise ValueError('No figure to save')
        
    def show(self,**kwargs):
        """
        Display the plot.

        Parameters
        ----------
        ``**kwargs``
            Additional keyword arguments passed to plt.show().
        """
        plt.show(**kwargs)

    def coverage_color(self):
        """Get the next color for a coverage area."""
        if self.config.coverage_color_default is None:
            return next(self.color_iterator)
        else:
            return self.config.coverage_color_default
        
    def handle_ranges(self,xrange,yrange):
        """
        Convert string labels to numeric indices for plotting.

        Parameters
        ----------
        xrange : list
            Range values for x-axis.
        yrange : list
            Range values for y-axis.

        Returns
        -------
        tuple
            Processed (xrange, yrange) with numeric values.
        """

        xlabel_dict = {normalize_string(value):idx for idx,value in enumerate(self.xlabels)}
        ylabel_dict = {normalize_string(value):idx for idx,value in enumerate(self.ylabels)}

        # Handle using labels for position
        for idx,x in enumerate(xrange):
            # If the user passed a string for the position
            if isinstance(x,str):
                # Normalize the key
                x = normalize_string(x)
                # Assign the xrange to its value as an integer
                xrange[idx] = xlabel_dict[x]
                # Add one to the max value of the xrange
                if idx == 1:
                    xrange[1]+=1

        for idx,y in enumerate(yrange):
            if isinstance(y,str):
                y = normalize_string(y)
                yrange[idx] = ylabel_dict[y]
                if idx == 1:
                    yrange[1]+=0.5
                if idx == 0:
                    yrange[0]-=0.5

        return xrange,yrange

    def init_figure(self) -> None:
        """
        Initialize figure and axes if not provided.
        """

        if self.fig is None and self.ax is None:
            # Standard 2D Matplotlib figure
            self.fig, self.ax = plt.subplots(figsize=self.figsize)

    def custom_ticks(self,labels,axis:str):
        """
        Set custom tick labels for specified axis.

        Parameters
        ----------
        labels : list
            List of tick labels.
        axis : str
            Axis to customize ('x' or 'y').
        """
        if axis.lower() == 'x':
            major_locator = self.ax.xaxis.set_major_locator
            label_setter = self.ax.set_xticklabels
            tick_positions = np.arange(0.5,len(labels)+0.5)  # Tick positions
            
        elif axis.lower() == 'y':
            major_locator = self.ax.yaxis.set_major_locator
            label_setter = self.ax.set_yticklabels  
            tick_positions = np.arange(0,len(labels))  # Tick positions     

        major_locator(FixedLocator(tick_positions))
        label_setter(labels)
        self.ax.tick_params('both',length=0)

    def set_padding(self):
        """Set plot limits with padding."""
        xmin = 0 - self.config.horizontal_padding
        xmax = len(self.xlabels) + self.config.horizontal_padding

        ymin = 0 - self.config.vertical_padding
        ymax = len(self.ylabels) - 1 + self.config.vertical_padding

        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)

    def add_grid(self, show_grid: bool):
        """Add grid to the plot if requested."""
        if show_grid:
            self.grid.add_grid(ax=self.ax)

    def set_up_plot(self,show_grid:bool=True):
        """
        Configure the plot with all necessary components.

        Parameters
        ----------
        show_grid : bool, optional
            Whether to show grid lines. Default is True.
        """
        
        # Init figure
        self.init_figure()
        # Set custom ticks and labels
        self.custom_ticks(labels=self.ylabels,axis='y')
        self.custom_ticks(labels=self.xlabels,axis='x')
        # Show the grid
        self.add_grid(show_grid)
        # Add padding to the border
        self.set_padding()
        # invert the y-xais
        self.ax.invert_yaxis()
        # Put the x-axis labels on top
        self.ax.tick_params(axis='x', labeltop=True, labelbottom=False)
        # Set layout to tight
        self.fig.tight_layout()

    def plot_coverages(self):
        """
        Plot all coverage areas on the figure.
        """
        for coverage in self.coverages:
            coverage.plot(self.ax)

    def plot(self,show_grid=True):
        """
        Create the complete coverage plot.

        Parameters
        ----------
        show_grid : bool, optional
            Whether to show grid lines. Default is True.
        """
        self.set_up_plot(show_grid=show_grid)
        self.plot_coverages()
