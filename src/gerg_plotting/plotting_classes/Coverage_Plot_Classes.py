# Coverage_Plot_Classes.py

import numpy as np
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
import inspect

from gerg_plotting.modules.utilities import extract_kwargs_with_aliases
from gerg_plotting.tools import normalize_string



@define
class Base:
    def _has_var(self, key) -> bool:
        '''Check if object has var'''
        return key in asdict(self).keys()
    
    def get_vars(self) -> list:
        '''Get list of object variables/attributes'''
        return list(asdict(self).keys())

    def __getitem__(self, key: str):
        '''
        Allow dictionary-style access to class attributes.
        
        Args:
            key (str): The attribute name to access.
        
        Returns:
            The value of the specified attribute.
        '''
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")  

    def __setitem__(self, key, value) -> None:
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")

    def __repr__(self) -> None:
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)



@define
class ExtentArrows(Base):
    # Defaults
    facecolor:str|tuple = field(default='black') # If "coverage_facecolor" then the arrow's facecolor will be the color of the corresponding coverage's facecolor
    edgecolor:str|tuple = field(default='black')
    width:float = field(default=0.05)
    head_width:float = field(default=0.12)
    zorder:float = field(default=2.9)
    linewidth:float = field(default=0)
    text_padding:float = field(default=0.05)
    # Add other defaults too
    # Arrows
    left_arrow:FancyArrow = field(default=None)
    right_arrow:FancyArrow = field(default=None)
    top_arrow:FancyArrow = field(default=None)
    bottom_arrow:FancyArrow = field(default=None)

    def calculate_arrow_length(self,ax:Axes,rect,text_left,text_right):
        rect_bbox = ax.transData.inverted().transform(rect.get_window_extent())

        rect_left, rect_bottom = rect_bbox[0]
        rect_right, rect_top = rect_bbox[1]

        left_arrow_length = rect_left-text_left-0.01
        right_arrow_length = rect_right-text_right-0.01

        return left_arrow_length,right_arrow_length


    def add_range_arrows(self,ax:Axes,text:Text,rect:Rectangle,**arrow_kwargs):
        
        if self.facecolor=='coverage_facecolor':
            self.facecolor = rect.get_facecolor()

        text_bbox = ax.transData.inverted().transform(text.get_window_extent())

        # Calculate the left and right bounds of the text in data coordinates
        text_left, text_bottom = text_bbox[0]
        text_right, text_top = text_bbox[1]
        text_y_center = (text_bottom + text_top) / 2  # The vertical center of the text

        arrow_props = {'width': self.width, 'facecolor': self.facecolor,'head_width':self.head_width,
                       "length_includes_head":True,'zorder':self.zorder,
                       'edgecolor':self.edgecolor,'linewidth':self.linewidth}

        left_arrow_length,right_arrow_length = (self.calculate_arrow_length(ax,rect,text_left=text_left,text_right=text_right))

        left_arrow_left_bound = text_left - (self.text_padding-0.03)  # Subtract a bit because arrow spills over a bit further than expected
        left_arrow_right_bound = left_arrow_length + self.text_padding

        right_arrow_left_bound = text_right + self.text_padding
        right_arrow_right_bound = right_arrow_length - self.text_padding

        left_arrow = FancyArrow(left_arrow_left_bound, text_y_center, left_arrow_right_bound, 0, **arrow_props)
        right_arrow = FancyArrow(right_arrow_left_bound, text_y_center, right_arrow_right_bound, 0, **arrow_props)

        ax.add_artist(left_arrow)
        ax.add_artist(right_arrow)


@define
class Grid(Base):
    xlabels:list
    ylabels:list
    # Defaults
    linewidth:float = field(default=1)
    linestyle:str = field(default='--')
    color:str|tuple = field(default='black')
    zorder:float = field(default=1.15)

    def add_hlines(self,ax:Axes,y_values,**kwargs):
        zorder = kwargs.pop('zorder',self.zorder)
        for y_value in y_values:
            ax.axhline(y_value,zorder=zorder,**kwargs)

    def add_vlines(self,ax:Axes,x_values,**kwargs):
        zorder = kwargs.pop('zorder',self.zorder)
        for x_value in x_values:
            ax.axvline(x_value,zorder=zorder,**kwargs)

    def add_grid(self,ax,**grid_kwargs):
        defaults = {('linewidth','lw'): self.linewidth,
                    ('color','c'): self.color,('linestyle','ls'): self.linestyle}

        linewidth, color, linestyle  = extract_kwargs_with_aliases(grid_kwargs, defaults).values()
        n_hlines = len(self.ylabels)
        n_vlines = len(self.xlabels)
        self.add_hlines(ax=ax,y_values=np.arange(-0.5,n_hlines+0.5,1),linewidth=linewidth,ls=linestyle,color=color)
        self.add_vlines(ax=ax,x_values=np.arange(0,n_vlines+1,1),linewidth=linewidth,ls=linestyle,color=color)


@define
class Coverage(Base):
    body:Rectangle = field(init=False)
    outline:Rectangle = field(init=False)
    label:Text = field(init=False)
    extent_arrows:ExtentArrows = field(init=False)

    # Body Default Parameters
    min_body_height:float = field(default=0.25)
    body_alpha:float = field(default=1)
    body_linewidth:float = field(default=1)
    body_color:str|tuple = field(default=None)
    body_hatch:str = field(default=None)
    # Outline Default Parameters
    outline_edgecolor:str|tuple = field(default='k')
    outline_alpha:float = field(default=1)
    # Label Default Parameters
    label_fontsize:float = field(default=11)



    def handle_ranges(self,xrange,yrange):
        '''
        If the user used label names/strings to identify the x and y ranges,
        we need to convert those to numeric so we can plot it
        '''

        xlabel_dict = {normalize_string(value):idx for idx,value in enumerate(xlabels)}
        ylabel_dict = {normalize_string(value):idx for idx,value in enumerate(ylabels)}

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

    def create(self,xrange,yrange,label,**kwargs):
        ''''''

        xrange,yrange = self.handle_ranges(xrange,yrange)

        # Bottom left corner
        anchor_point = (xrange[0],yrange[0])

        width = (xrange[1] - xrange[0])

        height = (yrange[1] - yrange[0])

        if height == 0:
            height = self.min_body_height

        rect_defaults = {('alpha','body_alpha'): self.body_alpha,('linewidth','lw','body_linewidth'): self.body_linewidth,
                    ('edgecolor','ec','outline_edgecolor'): self.outline_edgecolor,'label': label,
                    ('facecolor','fc'):self.body_color,'body_outline_alpha':self.outline_alpha,
                    ('hatch','body_hatch'):self.body_hatch}

        alpha, linewidth, outline_edgecolor, label, fc, coverage_outline_alpha, hatch  = extract_kwargs_with_aliases(kwargs, rect_defaults).values()

        rect_args = list(inspect.signature(Rectangle).parameters)
        rect_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in rect_args}

        # Init body
        body = Rectangle(anchor_point,width=width,height=height,
                         fc=fc,alpha=alpha,
                         linewidth=linewidth, edgecolor = None,
                         label=label,hatch=hatch,**rect_dict)
        
        # Init outline
        outline = Rectangle(anchor_point,width=width,height=height,fc=None,fill=False,alpha=coverage_outline_alpha,
                         linewidth=linewidth, edgecolor = outline_edgecolor,
                         label=None,zorder=body.get_zorder()+0.25,**rect_dict)
        

        text_args = list(inspect.signature(Text.set).parameters)+list(inspect.signature(Text).parameters)
        text_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in text_args}
        
        fontsize = text_dict.pop('fontsize',self.label_fontsize)
        label_position = kwargs.pop('label_position',body.get_center())

        text = Text(*label_position,text=label,fontsize=fontsize,ha='center',va='center',zorder=5,**text_dict)

        self.body = body
        self.outline = outline
        self.label = text

        self.extent_arrows = ExtentArrows()
        
        return self

    def plot(self,ax:Axes,**kwargs):
        ''''''
        ax.add_artist(self.body)
        ax.add_artist(self.outline)
        ax.add_artist(self.label)
        self.extent_arrows.add_range_arrows(ax=ax,text=self.label,rect=self.body,**kwargs)




@define
class CoveragePlot(Base):
    fig:Figure = field(default=None)
    ax:Axes = field(default=None)
    figsize:tuple = field(default=None)

    horizontal_padding:float = field(default=0.25)
    vertical_padding:float = field(default=0.75)

    xlabels:list = field(default=None)
    ylabels:list = field(default=None)

    cmap:str|Colormap = field(default='tab10')
    color_iterator:itertools.cycle = field(init=False)

    coverages:list[Coverage] = field(factory=list)

    grid:Grid = field(init=False)


    def __attrs_post_init__(self):
        self.grid = Grid(xlabels=self.xlabels,ylabels=self.ylabels)


    def add_coverage(self,xrange,yrange,label,**kwargs):
        '''
        xrange (list): A list of values containing the x coverage range
        yrange (list): A list of values containing the y coverage range

        Turn off the label on top of the coverage, but keep the label in the legend, pass `visible = False`
        '''
        # Init test values
        if not isinstance(xrange,list):
            xrange = [xrange]
        if not isinstance(yrange,list):
            yrange = [yrange]

        if len(xrange)==1:
            xrange.extend(xrange)
        if len(yrange)==1:
            yrange.extend(yrange)

        # If both xrange and yrange contain the same number of values
        if len(xrange) == len(yrange):
            # Init the coverage and add it to the list
            coverage = Coverage().create(xrange=xrange,yrange=yrange,label=label,**kwargs)
            self.coverages.extend([coverage])
            return
        else:
            raise ValueError(f'xrange and yrange must both be the same length {xrange = }, {yrange = }')
    

    def save(self,filename,**kwargs):
        '''
        Save the current figure
        '''
        if self.fig is not None:
            self.fig.savefig(fname=filename,**kwargs)
        else:
            raise ValueError('No figure to save')
        
    def show(self):
        '''
        Show all open figures
        '''
        plt.show()

    def init_figure(self) -> None:
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

        if self.fig is None and self.ax is None:
            # Standard 2D Matplotlib figure
            self.fig, self.ax = plt.subplots(figsize=self.figsize)

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
        xmax = len(self.xlabels)+self.horizontal_padding

        ymin = 0 - self.vertical_padding
        ymax = len(self.ylabels)-1+self.vertical_padding

        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)

    def add_grid(self,show_grid:bool,**grid_kwargs):
        if show_grid:
            self.grid.add_grid(ax=self.ax,**grid_kwargs)

    def set_up_plot(self,show_grid:bool=True,**grid_kwargs):
        # Init figure
        self.init_figure()
        # Set custom ticks and labels
        self.custom_ticks(labels=self.ylabels,axis='y')
        self.custom_ticks(labels=self.xlabels,axis='x')
        # Show the grid
        self.add_grid(show_grid,**grid_kwargs)
        # Add padding to the border
        self.set_padding()
        # invert the y-xais
        self.ax.invert_yaxis()
        # Put the x-axis labels on top
        self.ax.tick_params(axis='x', labeltop=True, labelbottom=False)
        # Set layout to tight
        self.fig.tight_layout()

    def plot_coverages(self,**kwargs):
        for coverage in self.coverages:
            coverage.plot(self.ax,**kwargs)

    def plot(self,show_grid=True,**kwargs):
        self.set_up_plot(show_grid=show_grid,**kwargs)
        self.plot_coverages(**kwargs)
        

cmap = plt.get_cmap('tab20')
domains = ['Regional_Local', 'All', 'Local', 'Basin_Regional', 'Basin_Local', 'Basin', 'Regional']
colors_light = [cmap(15),cmap(5),cmap(3),cmap(1),'yellow','pink','gold']

colors = colors_light
domain_colors = {key:value for key,value in zip(domains,colors)}
# Define the x and y labels
xlabels = ['Seconds','Minutes','Hours','Days','Weeks','Months','Years','Decades']
ylabels = ['Surface','10-100\nMeters','100-500\nMeters','Below 500\nMeters','Benthic']
# Init the coverage plotter
plotter = CoveragePlot(figsize=(12,6),xlabels=xlabels,ylabels=ylabels)
plotter.add_coverage(['Hours','Decades'],['Surface','Benthic'],label='Agency',label_position=(4,3.3),fc=domain_colors['All'])
plotter.add_coverage(['Days','Months'],['Surface','Benthic'],label='Marine Services',fc=domain_colors['Regional_Local'])
plotter.plot()