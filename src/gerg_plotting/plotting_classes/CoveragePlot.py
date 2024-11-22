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



from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.modules.utilities import extract_kwargs_with_aliases


@define
class CoveragePlot(Plotter):
    x_labels:list = field(default=None)
    y_labels:list = field(default=None)

    colormap:matplotlib.colors.Colormap = field(default=None)
    n_colors:int = field(default=None)
    color_iterator:itertools.cycle = field(init=False)


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
            self.n_colors = 10
        self.color_iterator = itertools.cycle(
            (self.colormap(i / (self.n_colors - 1)) for i in range(self.n_colors))
        )


    def coverage_color(self):
        """
        A generator that yields the next color in the colormap cycle.

        :yield: A tuple representing an RGBA color.
        """
        return next(self.color_iterator)


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

    def set_padding(self,padding):
        xmin = 0 -padding
        xmax = len(self.x_labels)+padding

        ymin = -1 - padding
        ymax = len(self.y_labels)+padding

        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)

    def init_figure(self, fig=None, ax=None, figsize=(10, 6)) -> None:
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
            # Standard 2D Matplotlib figure with no projection
            self.fig, self.ax = plt.subplots(figsize=figsize)
                
        elif fig is not None and ax is not None:
            # Use existing figure and axes
            self.fig = fig
            self.ax = ax


    def set_up_plot(self,fig,ax,padding=0.15):
        # Init figure
        self.init_figure(fig=fig,ax=ax)
        # Set custom ticks and labels
        self.custom_ticks(labels=self.y_labels,axis='y')
        self.custom_ticks(labels=self.x_labels,axis='x')
        # Add padding to the border
        self.set_padding(padding)
        # invert the y-xais
        self.ax.invert_yaxis()


    def add_rectangle(self,x_range,y_range,**kwargs):
        # Bottom left corner
        anchor_point = (x_range[0],y_range[0])

        width = (x_range[1] - x_range[0])

        height = (y_range[1] - y_range[0]) + 0.25

        defaults = {'alpha': 0.85,('linewidth','lw'): 1,('edgecolor','ec'): 
                    'k','label': None,('facecolor','fc'):self.coverage_color(),
                    ('fontsize','label_fontsize'):11}

        alpha, linewidth, edgecolor, label, fc, fontsize  = extract_kwargs_with_aliases(kwargs, defaults).values()


        rect_args = list(inspect.signature(matplotlib.patches.Rectangle).parameters)
        rect_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in rect_args}

        rect = Rectangle(anchor_point,width=width,height=height,
                         fc=fc,alpha=alpha,
                         linewidth=linewidth, edgecolor = edgecolor,
                         label=label,**rect_dict)
        
        text_args = list(inspect.signature(matplotlib.text.Text.set).parameters)+list(inspect.signature(matplotlib.text.Text).parameters)
        text_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in text_args}
        
        self.ax.text(*rect.get_center(),s=label,ha='center',va='center',fontsize=fontsize,**text_dict)

        self.ax.add_patch(rect)

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
        len_x_range = len(x_range)
        len_y_range = len(y_range)

        # If both x_range and y_range contain the same number of values, we will plot and return early
        if len_x_range == len_y_range:
            self.add_rectangle(x_range,y_range,**kwargs)
            return
        else:
            raise ValueError(f'x-range and y_range must both be the same length')

