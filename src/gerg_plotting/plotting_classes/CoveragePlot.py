import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import matplotlib.patches
import matplotlib.text
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.patches import Rectangle
from attrs import define,field
import itertools
import inspect
import re


from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.modules.utilities import extract_kwargs_with_aliases


def normalize_string(input_string: str) -> str:
    """
    Normalizes a string by performing the following actions:
    - Converts the string to lowercase.
    - Replaces spaces, newlines, and other specified characters with underscores.
    - Removes leading and trailing underscores.
    - Collapses multiple consecutive underscores into a single underscore.

    Parameters:
    input_string (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")
    
    # Define the characters to be replaced by underscores
    replace_pattern = r"[ \t\n\r\f\v.,;:!@#$%^&*()+=?/<>|\\\"'`~\[\]{}]"
    
    # Convert to lowercase
    normalized = input_string.lower()
    
    # Replace specified characters with underscores
    normalized = re.sub(replace_pattern, "_", normalized)
    
    # Collapse multiple underscores into one
    normalized = re.sub(r"__+", "_", normalized)
    
    # Remove leading and trailing underscores
    normalized = normalized.strip("_")
    
    return normalized


@define
class CoveragePlot(Plotter):
    '''
    A 2-d Categorical plot showing the coverage through categories
    '''
    x_labels:list = field(default=None)
    y_labels:list = field(default=None)

    x_label_dict:dict = field(init=False)
    y_label_dict:dict = field(init=False)

    colormap:matplotlib.colors.Colormap = field(default=None)
    n_colors:int = field(default=None)
    color_iterator:itertools.cycle = field(init=False)

    patches:list = field(init=False)

    # Default figure/axes Parameters
    horizontal_padding:float = field(default=0.25)
    vertical_padding:float = field(default=0.75)

    # Default Coverage Parameters
    figsize:tuple = field(default=(10,6))
    coverage_alpha:float = field(default=0.85)
    coverage_linewidth:float = field(default=1.0)
    coverage_edgecolor:str|tuple = field(default='k')
    coverage_label:str|None = field(default=None)
    coverage_fontsize:float|int = field(default=11)
    coverage_color_default:str|tuple = field(default=None)
    coverage_min_rectangle_height:float = field(default=0.25)

    # Default Grid Parameters
    grid_linestyle:str = field(default='--')
    grid_linewidth:float = field(default=1)
    grid_color:str|tuple = field(default='gray')


    def __attrs_post_init__(self):
        """
        Initializes the ColorCycler.

        :param colormap_name: Name of the matplotlib colormap to use.
        :param n_colors: Number of discrete colors to divide the colormap into.
        """
        if self.colormap is None:
            self.colormap = plt.get_cmap('tab10')
        elif isinstance(self.colormap,str):
            self.colormap = plt.get_cmap(self.colormap)
        elif isinstance(self.colormap,matplotlib.colors.Colormap):
            self.colormap = self.colormap
        if self.n_colors is None:
            self.n_colors = self.colormap.N
        self.color_iterator = itertools.cycle(
            (self.colormap(i / (self.n_colors - 1)) for i in range(self.n_colors))
        )

        self.x_label_dict = {normalize_string(value):idx for idx,value in enumerate(self.x_labels)}
        self.y_label_dict = {normalize_string(value):idx for idx,value in enumerate(self.y_labels)}

        self.patches = list([])


    def coverage_color(self):
        """
        A generator that yields the next color in the colormap cycle.

        :yield: A tuple representing an RGBA color.
        """
        if self.coverage_color_default is None:
            return next(self.color_iterator)
        else:
            return self.coverage_color_default


    def custom_ticks(self,labels,axis:str):
        # Set custom ticks and labels

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
        xmin = 0 - self.horizontal_padding
        xmax = len(self.x_labels)+self.horizontal_padding

        ymin = 0 - self.vertical_padding
        ymax = len(self.y_labels)-1+self.vertical_padding

        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)

    def init_figure(self, fig=None, ax=None) -> None:
        '''
        Initialize the figure and axes if they are not provided.
        
        Args:
            fig (matplotlib.figure.Figure, optional): Pre-existing figure.
            ax (matplotlib.axes.Axes, optional): Pre-existing axes.
            three_d (bool, optional): Flag to initialize a 3D plot.
            geography (bool, optional): Flag to initialize a map projection (Cartopy).
        
        Raises:
            ValueError: If both 'three_d' and 'geography' are set to True.
        '''

        if fig is None and ax is None:
            # Standard 2D Matplotlib figure
            self.fig, self.ax = plt.subplots(figsize=self.figsize)
                
        elif fig is not None and ax is not None:
            # Use existing figure and axes
            self.fig = fig
            self.ax = ax

    def add_grid(self,show_grid,grid_kwargs):
        if show_grid:
            defaults = {('linewidth','lw'): self.grid_linewidth,
                        ('color','c'): self.grid_color,('linestyle','ls'): self.grid_linestyle}

            linewidth, color, linestyle  = extract_kwargs_with_aliases(grid_kwargs, defaults).values()
            n_hlines = len(self.y_labels)
            n_vlines = len(self.x_labels)
            self.add_hlines(np.arange(-0.5,n_hlines+0.5,1),linewidth=linewidth,ls=linestyle,color=color)
            self.add_vlines(np.arange(0,n_vlines+1,1),linewidth=linewidth,ls=linestyle,color=color)


    def set_up_plot(self,fig=None,ax=None,show_grid:bool=True,**grid_kwargs):
        # Init figure
        self.init_figure(fig=fig,ax=ax)
        # Set custom ticks and labels
        self.custom_ticks(labels=self.y_labels,axis='y')
        self.custom_ticks(labels=self.x_labels,axis='x')
        # Show the grid
        self.add_grid(show_grid,grid_kwargs)
        # Add padding to the border
        self.set_padding()
        # invert the y-xais
        self.ax.invert_yaxis()
        # Put the x-axis labels on top
        self.ax.tick_params(axis='x', labeltop=True, labelbottom=False)
        # Set layout to tight
        self.fig.tight_layout()

    
    def handle_ranges(self,x_range,y_range):
        '''
        If the user used label names/strings to identify the x and y ranges,
        we need to convert those to numeric so we can plot it
        '''

        # Handle using labels for position
        for idx,x in enumerate(x_range):
            if isinstance(x,str):
                x = normalize_string(x)
                x_range[idx] = self.x_label_dict[x]
                if idx == 1:
                    x_range[1]+=1

                
        for idx,y in enumerate(y_range):
            if isinstance(y,str):
                y = normalize_string(y)
                y_range[idx] = self.y_label_dict[y]
                if idx == 1:
                    y_range[1]+=0.5
                if idx == 0:
                    y_range[0]-=0.5

        return x_range,y_range



    def make_rectangle(self,x_range,y_range,**kwargs):

        x_range,y_range = self.handle_ranges(x_range,y_range)

        # Bottom left corner
        anchor_point = (x_range[0],y_range[0])

        width = (x_range[1] - x_range[0])

        height = (y_range[1] - y_range[0])

        if height == 0:
            height = self.coverage_min_rectangle_height

        defaults = {'alpha': self.coverage_alpha,('linewidth','lw'): self.coverage_linewidth,
                    ('edgecolor','ec'): self.coverage_edgecolor,'label': self.coverage_label,
                    ('facecolor','fc'):self.coverage_color(),
                    ('fontsize','label_fontsize'):self.coverage_fontsize}

        alpha, linewidth, edgecolor, label, fc, fontsize  = extract_kwargs_with_aliases(kwargs, defaults).values()

        rect_args = list(inspect.signature(matplotlib.patches.Rectangle).parameters)
        rect_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in rect_args}

        rect = Rectangle(anchor_point,width=width,height=height,
                         fc=fc,alpha=alpha,
                         linewidth=linewidth, edgecolor = edgecolor,
                         label=label,**rect_dict)
        

        text_args = list(inspect.signature(matplotlib.text.Text.set).parameters)+list(inspect.signature(matplotlib.text.Text).parameters)
        text_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in text_args}
        
        text = matplotlib.text.Text(*rect.get_center(),text=label,ha='center',va='center',**text_dict)
        
        self.patches.append([rect,text])


    def add_hlines(self,y_values,**kwargs):
        zorder = kwargs.pop('zorder',0)
        for y_value in y_values:
            self.ax.axhline(y_value,zorder=zorder,**kwargs)

    def add_vlines(self,x_values,**kwargs):
        zorder = kwargs.pop('zorder',0)
        for x_value in x_values:
            self.ax.axvline(x_value,zorder=zorder,**kwargs)


    def add_coverage(self,x_range,y_range,**kwargs):
        '''
        x_range (list): A list of values containing the x coverage range
        y_range (list): A list of values containing the y coverage range

        Turn off the label on top of the coverage, but keep the label in the legend, pass `visible = False`
        '''
        # Init test values
        if not isinstance(x_range,list):
            x_range = [x_range]
        if not isinstance(y_range,list):
            y_range = [y_range]

        if len(x_range)==1:
            x_range.extend(x_range)
        if len(y_range)==1:
            y_range.extend(y_range)

        # If both x_range and y_range contain the same number of values, we will plot and return early
        if len(x_range) == len(y_range):
            self.make_rectangle(x_range,y_range,**kwargs)
            return
        else:
            raise ValueError(f'x_range and y_range must both be the same length {x_range = }, {y_range = }')


    def plot(self):
        '''
        Only call after you have added all of your coverages
        '''
        self.set_up_plot()  
        for rect,text in self.patches:
            self.ax.add_patch(rect)
            self.ax.add_artist(text)


