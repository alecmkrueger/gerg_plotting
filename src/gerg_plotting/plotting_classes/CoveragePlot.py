import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.patches import Rectangle,Polygon
from attrs import define,field
import itertools

from gerg_plotting.modules.utilities import extract_kwargs,extract_kwargs_with_aliases


@define
class CoveragePlot():
    x_labels:list = field(default=None)
    y_labels:list = field(default=None)

    fig: matplotlib.figure.Figure = field(default=None)
    ax: matplotlib.axes.Axes = field(default=None)

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


    def set_up_plot(self,fig,ax):
        # Init figure
        self.init_figure(fig=fig,ax=ax)
        # Set custom ticks and labels
        self.custom_ticks(labels=self.y_labels,axis='y')
        self.custom_ticks(labels=self.x_labels,axis='x')
        # Add padding to the border
        self.set_padding(0.15)
        # invert the y-xais
        self.ax.invert_yaxis()


    def add_rectangle(self,x_range,y_range,**kwargs):
        # Bottom left corner
        anchor_point = (x_range[0],y_range[0])

        width = (x_range[1] - x_range[0])

        height = (y_range[1] - y_range[0]) + 0.25

        defaults = {'alpha': 0.85,('linewidth','lw'): 1,('edgecolor','ec'): 
                    'k','label': None,('facecolor','fc'):self.coverage_color()}

        alpha, linewidth, edgecolor, label, fc = extract_kwargs_with_aliases(kwargs, defaults).values()

        rect = Rectangle(anchor_point,width=width,height=height,
                         fc=fc,alpha=alpha,
                         linewidth=linewidth, edgecolor = edgecolor,
                         label=label,**kwargs)
        
        self.ax.text(*rect.get_center(),s=label,ha='center',va='center')

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


# palette = ['#275C62', '#298880', '#5AA786','#8AB17D','#E9C46A','#F4A261','#E76F51']
# palette = ['#298880', '#8AB17D', '#BABB74','#E9C46A','#F4A261','#EE8959','#E76F51']

# cmap = matplotlib.colors.ListedColormap(palette)
# n_colors = len(palette)

cmap = 'tab20'
n_colors = 20

x_labels = ['Seconds','Minutes','Hours','Days','Weeks','Month','Years','Decades']
y_labels = ['Surface','10-100\nmeters','100-500\nmeters','Below 500\nmeters','Benthos']


fig,ax = plt.subplots(figsize=(11,7))

plotter = CoveragePlot(x_labels=x_labels,y_labels=y_labels,
             colormap=cmap,n_colors=n_colors)
# Init plot with the x and y labels and the axes bounds limit
plotter.set_up_plot(fig=fig,ax=ax)
# Add grid
plotter.add_hlines(np.arange(-0.5,5.5,1),linewidth=1.25,ls='--',color='gray')
plotter.add_vlines(np.arange(0,9,1),linewidth=1.25,ls='--',color='gray')
# All Depths
plotter.add_coverage(x_range=[7,8],y_range=[-0.45,4.2],label='Climate\nScience')
plotter.add_coverage(x_range=[5,6],y_range=[-0.45,4.2],label='Fisheries')
# Surface
plotter.add_coverage(x_range=[3,7],y_range=[-0.15,-0.15],label='Oil and Gas')
plotter.add_coverage(x_range=[2,3],y_range=[-0.45,-0.45],label='SAR')
plotter.add_coverage(x_range=[3,7],y_range=[0.15,0.15],label='Wind and Algal Blooms')
# 10-100m
plotter.add_coverage(x_range=[2,4],y_range=[0.85,0.85],label='Hurricane Forcasting')
plotter.add_coverage(x_range=[3,6],y_range=[1.15,1.15],label='Hypoxia')
# 100-500m
plotter.add_coverage(x_range=[0,3],y_range=[2,3],label='Example')
plotter.ax.texts[7].set_fontsize(20)
# Below 500m
plotter.add_coverage(x_range=[3,7],y_range=[3,3],label='Oil and Gas',fc=plotter.colormap(2))
