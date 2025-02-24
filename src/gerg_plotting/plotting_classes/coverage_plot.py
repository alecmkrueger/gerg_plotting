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
    """Color of arrow fill. Use 'coverage_color' to match coverage color."""
    
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
    
    label_background_pad: float = 2
    """Padding around label background."""
    
    label_background_linewidth: float = 0
    """Width of label background border."""
    
    label_background_alpha: float = 1
    """Transparency of label background."""
    
    _label_background_color: float = 'body_color'
    """Color of label background."""
    
    show_arrows: bool = True
    """Whether to show extent arrows."""


    @property
    def label_background_color(self):
        """Get the label background color."""
        if self._label_background_color == 'body_color':
            return self.body_color
        return self
    
    @label_background_color.setter
    def label_background_color(self, value):
        """Set the label background color."""
        self._label_background_color = value

@define
class CoveragePlotConfig(BaseConfig):
    """Configuration for overall coverage plot."""
    
    horizontal_padding: float = 0.25
    """Padding on left and right of plot."""
    
    vertical_padding: float = 0.75
    """Padding on top and bottom of plot."""
    
    coverage_color_default: str|tuple = None
    """Default color for coverages if specified."""


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
    xlabels:list
    ylabels:list
    _config: GridConfig = field(factory=GridConfig)
    
    @property
    def config(self) -> GridConfig:
        """Access and modify grid styling configuration."""
        return self._config
    
    @config.setter
    def config(self, value: dict | GridConfig):
        if isinstance(value, dict):
            self._config = GridConfig(**value)
        else:
            self._config = value

    def add_hlines(self,ax:Axes,y_values,**kwargs):
        """
        Add horizontal lines to the plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to draw the lines on.
        y_values : array-like
            Y-coordinates where horizontal lines should be drawn.
        ``**kwargs``
            Additional keyword arguments passed to axhline.
        """
        zorder = kwargs.pop('zorder',self.config.grid_zorder)
        for y_value in y_values:
            ax.axhline(y_value,zorder=zorder,**kwargs)

    def add_vlines(self,ax:Axes,x_values,**kwargs):
        """
        Add vertical lines to the plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to draw the lines on.
        x_values : array-like
            X-coordinates where vertical lines should be drawn.
        ``**kwargs``
            Additional keyword arguments passed to axvline.
        """
        zorder = kwargs.pop('zorder',self.config.grid_zorder)
        for x_value in x_values:
            ax.axvline(x_value,zorder=zorder,**kwargs)

    def add_grid(self,ax,**grid_kwargs):
        """
        Add complete grid to the plot with both horizontal and vertical lines.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to draw the grid on.
        ``**grid_kwargs``
            Additional keyword arguments for grid customization including:
            - grid_linewidth: Width of grid lines
            - grid_color: Color of grid lines
            - grid_linestyle: Style of grid lines
        """
        defaults = {
            'grid_linewidth': self.config.grid_linewidth,
            'grid_color': self.config.grid_color,
            'grid_linestyle': self.config.grid_linestyle
        }

        linewidth, color, linestyle  = extract_kwargs_with_aliases(grid_kwargs, defaults).values()
        n_hlines = len(self.ylabels)
        n_vlines = len(self.xlabels)
        self.add_hlines(ax=ax,y_values=np.arange(-0.5,n_hlines+0.5,1),linewidth=linewidth,ls=linestyle,color=color)
        self.add_vlines(ax=ax,x_values=np.arange(0,n_vlines+1,1),linewidth=linewidth,ls=linestyle,color=color)

@define
class ExtentArrows(Base):
    """A class for managing and drawing arrows that indicate coverage extents."""
    label_position:tuple = field(default=None)
    left_arrow: FancyArrow = field(default=None)
    right_arrow: FancyArrow = field(default=None)
    top_arrow: FancyArrow = field(default=None)
    bottom_arrow: FancyArrow = field(default=None)

    _config: ExtentArrowConfig = field(factory=ExtentArrowConfig)
    
    @property
    def config(self) -> ExtentArrowConfig:
        """Access and modify arrow styling configuration."""
        return self._config
    
    @config.setter
    def config(self, value: dict | ExtentArrowConfig):
        if isinstance(value, dict):
            self._config = ExtentArrowConfig(**value)
        else:
            self._config = value

    def calculate_arrow_length(self,ax:Axes,rect,text_left,text_right):
        """
        Calculate the lengths needed for extent arrows.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes containing the arrows.
        rect : Rectangle
            Rectangle object representing coverage area.
        text_left : float
            Left boundary of text.
        text_right : float
            Right boundary of text.

        Returns
        -------
        tuple
            (left_arrow_length, right_arrow_length)
        """
        rect_bbox = ax.transData.inverted().transform(rect.get_window_extent())

        rect_left, rect_bottom = rect_bbox[0]
        rect_right, rect_top = rect_bbox[1]

        left_arrow_length = rect_left-text_left
        right_arrow_length = rect_right-text_right

        return left_arrow_length,right_arrow_length


    def add_range_arrows(self, ax: Axes, text: Text, rect: Rectangle):
        """Add arrows indicating the range of coverage."""
        
        if self.config.arrow_facecolor == 'coverage_color':
            self.config.arrow_facecolor = rect.get_facecolor()
        elif self.config.arrow_facecolor == 'hatch_color':
            self.config.arrow_facecolor = rect.get_edgecolor()

        text_bbox = ax.transData.inverted().transform(text.get_window_extent())
        text_left, text_bottom = text_bbox[0]
        text_right, text_top = text_bbox[1]
        text_y_center = (text_bottom + text_top) / 2

        arrow_props = {
            'width': self.config.arrow_tail_width,
            'facecolor': self.config.arrow_facecolor,
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
    extent_arrows: ExtentArrows = field(init=False)
    anchor_point: tuple[float, float] = field(init=False)
    width: float = field(init=False)
    height: float = field(init=False)

    _config: CoverageConfig = field(factory=CoverageConfig)
    
    @property
    def config(self) -> CoverageConfig:
        """Access and modify coverage styling configuration."""
        return self._config
    
    @config.setter
    def config(self, value: dict | CoverageConfig):
        if isinstance(value, dict):
            self._config = CoverageConfig(**value)
        else:
            self._config = value

    def create(self, xrange, yrange, label, **kwargs):
        """Create a new coverage object with specified range and label."""
        self._update_configs_from_kwargs(kwargs)
        self._calculate_dimensions(xrange, yrange)
        self._create_body()
        self._create_outline()
        self._create_label(label, kwargs.get('label_position', None))
        self._create_arrows(kwargs)
        return self

    def _update_configs_from_kwargs(self, kwargs):
        """Update configurations from provided kwargs."""
        body_defaults = {
            'body_alpha': self.config.body_alpha,
            'body_linewidth': self.config.body_linewidth,
            'body_color': self.config.body_color,
            'body_hatch': self.config.body_hatch,
            'body_hatch_color': self.config.body_hatch_color,
            'hatch_linewidth': self.config.hatch_linewidth,
            'body_min_height': self.config.body_min_height
        }
        outline_defaults = {
            'outline_edgecolor': self.config.outline_edgecolor,
            'body_outline_alpha': self.config.outline_alpha,
            'outline_linewidth': self.config.outline_linewidth
        }
        
        # Extract and update configs
        self.config = extract_kwargs_with_aliases(kwargs, {**body_defaults, **outline_defaults})

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

    def _create_label(self, label, position=None):
        """Create the coverage label."""
        position = position or self.body.get_center()
        self.label = Text(
            *position, text=label,
            fontsize=self.config.label_fontsize,
            ha='center', va='center', zorder=5
        )

    def _create_arrows(self, kwargs):
        """Create extent arrows if enabled."""
        if self.config.show_arrows:
            self.extent_arrows = ExtentArrows(**kwargs)

    
    def _add_label_background(self,text:Text):
        """
        Add background to coverage label.

        Parameters
        ----------
        text : matplotlib.text.Text
            The text object to add background to.
        """
        print(dict(facecolor=self.config.label_background_color,pad=self.config.label_background_pad,
                           linewidth=self.config.label_background_linewidth,alpha=self.config.label_background_alpha))
        text.set_bbox(dict(facecolor=self.config.label_background_color,pad=self.config.label_background_pad,
                           linewidth=self.config.label_background_linewidth,alpha=self.config.label_background_alpha))

    def plot(self,ax:Axes,**kwargs):
        """
        Plot the coverage on given axes.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot on.
        ``**kwargs``
            Additional keyword arguments for plotting.
        """
        ax.add_artist(self.body)
        ax.add_artist(self.outline)
        ax.add_artist(self.label)
        self._add_label_background(self.label)
        if self.config.show_arrows:
            self.extent_arrows.add_range_arrows(ax=ax,text=self.label,rect=self.body,**kwargs)


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

    _config: CoveragePlotConfig = field(factory=CoveragePlotConfig)
    
    @property
    def config(self) -> CoveragePlotConfig:
        """Access and modify plot styling configuration."""
        return self._config
    
    @config.setter
    def config(self, value: dict | CoveragePlotConfig):
        if isinstance(value, dict):
            # Handle CoverageConfig attributes
            coverage_attrs = {k: v for k, v in value.items() 
                           if hasattr(CoverageConfig(), k)}
            print(f"Setting coverage attributes: {coverage_attrs}")
            if coverage_attrs:
                for coverage in self.coverages:
                    coverage.config = coverage_attrs

            # Handle GridConfig attributes
            grid_attrs = {k: v for k, v in value.items() 
                        if hasattr(GridConfig(), k)}
            print(f"Setting grid attributes: {grid_attrs}")
            if grid_attrs:
                self.grid.config = grid_attrs

            # Handle ExtentArrowConfig attributes
            arrow_attrs = {k: v for k, v in value.items()
                         if hasattr(ExtentArrowConfig(), k)}
            print(f"Setting arrow attributes: {arrow_attrs}")
            if arrow_attrs:
                for coverage in self.coverages:
                    if coverage.extent_arrows:
                        coverage.extent_arrows.config = arrow_attrs

            # Handle remaining CoveragePlotConfig attributes
            plot_attrs = {k: v for k, v in value.items() 
                        if hasattr(CoveragePlotConfig(), k)}
            print(f"Setting plot attributes: {plot_attrs}")
            if plot_attrs:
                self._config = CoveragePlotConfig(**plot_attrs)
        else:
            self._config = value



    def __attrs_post_init__(self):
        """
        Initializes the ColorCycler and the coverages container

        :param colormap_name: Name of the matplotlib colormap to use.
        :param n_colors: Number of discrete colors to divide the colormap into.
        """
        if self.cmap is None:
            self.cmap = plt.get_cmap('tab10')
        elif isinstance(self.cmap,str):
            self.cmap = plt.get_cmap(self.cmap)
        elif isinstance(self.cmap,Colormap):
            self.cmap = self.cmap
        n_colors = self.cmap.N
        self.color_iterator = itertools.cycle(
            (self.cmap(i / (n_colors - 1)) for i in range(n_colors))
        )

        self.grid = Grid(xlabels=self.xlabels,ylabels=self.ylabels)

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

    def add_coverage(self, xrange, yrange, label=None, **kwargs):
        """Add a new coverage area to the plot."""
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
            
            # Separate config kwargs from other kwargs
            config_kwargs, other_kwargs = self._extract_config_kwargs(kwargs)
            
            # Create new coverage with config
            coverage = Coverage()
            coverage.config = config_kwargs
            coverage.config.body_color = config_kwargs.pop('body_color', self.coverage_color())
            print(f"Coverage config: {coverage.config}")
            coverage = coverage.create(xrange=xrange, yrange=yrange, label=label, **other_kwargs)
            
            self.coverages.append(coverage)
            return
            
        raise ValueError(f'xrange and yrange must both be the same length {xrange = }, {yrange = }')


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
        """
        Get the next color for a coverage area.

        Returns
        -------
        tuple or str
            RGBA color tuple or specified default color.
        """
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
        """
        Set plot limits with padding.
        """
        xmin = 0 - self.config.horizontal_padding
        xmax = len(self.xlabels)+self.config.horizontal_padding

        ymin = 0 - self.config.vertical_padding
        ymax = len(self.ylabels)-1+self.config.vertical_padding

        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)

    def add_grid(self,show_grid:bool):
        """
        Add grid to the plot if requested.

        Parameters
        ----------
        show_grid : bool
            Whether to show the grid.
        """
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
