import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import matplotlib.patches
import matplotlib.text
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.patches import Rectangle,FancyArrow
from attrs import define,field
import itertools
import inspect


from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.modules.utilities import extract_kwargs_with_aliases
from gerg_plotting.tools import normalize_string

def show_color_swatch(color,title):
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.add_patch(Rectangle((0, 0), 1, 1, color=color))
    ax.axis('off')
    ax.set_title(title)
    fig.show()

@define(auto_attribs=True)
class Coverage:
    """
    Encapsulates a rectangle, its outline, associated text, and range arrows.
    """
    rect: Rectangle
    rect_outline: Rectangle
    text: matplotlib.text.Text
    left_arrow: FancyArrow
    right_arrow: FancyArrow

    @staticmethod
    def create(anchor_point, width, height, label, 
               alpha, linewidth, edgecolor, fc, coverage_outline_alpha, 
               hatch, fontsize, label_position, ax:matplotlib.axes.Axes,
               arrow_width, arrow_facecolor, arrow_head_width, 
               arrow_length_includes_head, arrow_zorder, arrow_edge_color, 
               arrow_linewidth, arrow_text_padding, text_padding, **kwargs):
        """
        Factory method to create a Coverage instance.
        
        Args:
            anchor_point (tuple): Bottom-left corner of the rectangle.
            width (float): Width of the rectangle.
            height (float): Height of the rectangle.
            label (str): Text label for the rectangle.
            alpha (float): Alpha value for rectangle fill.
            linewidth (float): Line width for outline.
            edgecolor (str): Color of the outline.
            fc (str): Fill color for the rectangle.
            coverage_outline_alpha (float): Alpha value for the outline rectangle.
            hatch (str): Hatch pattern for the rectangle.
            fontsize (int): Font size for the label text.
            label_position (tuple): Position for the label text.
            ax (matplotlib.axes.Axes): The axes on which the elements are drawn.
            arrow_width (float): Width of the arrows.
            arrow_facecolor (str): Fill color for the arrows.
            arrow_head_width (float): Width of the arrowhead.
            arrow_length_includes_head (bool): Whether the arrow length includes the head.
            arrow_zorder (float): Z-order for the arrows.
            arrow_edge_color (str): Edge color for the arrows.
            arrow_linewidth (float): Line width for the arrows.
            arrow_text_padding (float): Padding between the arrows and the text.
            text_padding (float): Additional text padding.
            **kwargs: Additional keyword arguments for the rectangle and text.

        Returns:
            Coverage: A new instance of the class.
        """
        # Separate kwargs for rect and text
        rect_args = list(Rectangle.__init__.__code__.co_varnames)
        text_args = list(matplotlib.text.Text.__init__.__code__.co_varnames)

        rect_kwargs = {k: kwargs.pop(k) for k in list(kwargs) if k in rect_args}
        text_kwargs = {k: kwargs.pop(k) for k in list(kwargs) if k in text_args}

        rect = Rectangle(anchor_point, width=width, height=height,
                         fc=fc, alpha=alpha, linewidth=linewidth,
                         edgecolor=None, label=label, hatch=hatch, **rect_kwargs)

        rect_outline = Rectangle(anchor_point, width=width, height=height, 
                                 fc=None, fill=False, alpha=coverage_outline_alpha,
                                 linewidth=linewidth, edgecolor=edgecolor,
                                 label=None, zorder=rect.get_zorder() + 0.25, **rect_kwargs)

        text = matplotlib.text.Text(*label_position, text=label, fontsize=fontsize,
                                    ha='center', va='center', zorder=5, **text_kwargs)

        if arrow_facecolor == 'coverage_facecolor':
            arrow_facecolor = rect.get_facecolor()

        text_bbox = ax.transData.inverted().transform(text.get_window_extent())

        text_left, text_bottom = text_bbox[0]
        text_right, text_top = text_bbox[1]
        text_y_center = (text_bottom + text_top) / 2

        arrow_props = {
            'width': arrow_width,
            'facecolor': arrow_facecolor,
            'head_width': arrow_head_width,
            'length_includes_head': arrow_length_includes_head,
            'zorder': arrow_zorder,
            'edgecolor': arrow_edge_color,
            'linewidth': arrow_linewidth
        }

        rect_bbox = ax.transData.inverted().transform(rect.get_window_extent())

        rect_left, _ = rect_bbox[0]
        rect_right, _ = rect_bbox[1]

        left_arrow_length = rect_left - text_left - 0.01
        right_arrow_length = rect_right - text_right - 0.01

        left_arrow_left_bound = text_left - (arrow_text_padding - 0.03)
        left_arrow_right_bound = left_arrow_length + arrow_text_padding

        right_arrow_left_bound = text_right + arrow_text_padding
        right_arrow_right_bound = right_arrow_length - arrow_text_padding

        left_arrow = FancyArrow(left_arrow_left_bound, text_y_center, left_arrow_right_bound, 0, **arrow_props)
        right_arrow = FancyArrow(right_arrow_left_bound, text_y_center, right_arrow_right_bound, 0, **arrow_props)

        # ax.add_artist(left_arrow)
        # ax.add_artist(right_arrow)

        return Coverage(rect, rect_outline, text, left_arrow, right_arrow)

    def format_coverage_label(self, text: matplotlib.text.Text, pad, linewidth, alpha):
        """
        Formats the coverage label with a background matching the rectangle's face color.

        Args:
            text (matplotlib.text.Text): The label text.
            pad (float): Padding around the text.
            linewidth (float): Line width for the text background.
            alpha (float): Alpha value for the text background.
        """
        text.set_bbox({
            'facecolor': self.rect.get_facecolor(),
            'pad': pad,
            'linewidth': linewidth,
            'alpha': alpha
        })




    





@define
class CoveragePlot(Plotter):
    '''
    A 2-d Categorical plot showing the coverage through categories
    '''
    x_labels:list = field(default=None)
    y_labels:list = field(default=None)
    figsize:tuple = field(default=(10,6))

    x_label_dict:dict = field(init=False)
    y_label_dict:dict = field(init=False)

    colormap:matplotlib.colors.Colormap = field(default=None)
    n_colors:int = field(default=None)
    color_iterator:itertools.cycle = field(init=False)

    patches:list[Coverage] = field(init=False)

    # Default figure/axes Parameters
    horizontal_padding:float = field(default=0.25)
    vertical_padding:float = field(default=0.75)

    # Default Coverage Parameters
    coverage_alpha:float = field(default=0.85)
    coverage_linewidth:float = field(default=1)
    coverage_edgecolor:str|tuple = field(default='k')
    coverage_label:str|None = field(default=None)
    coverage_fontsize:float|int = field(default=11)
    coverage_color_default:str|tuple = field(default=None)
    coverage_min_rectangle_height:float = field(default=0.25)
    coverage_outline_alpha:float = field(default=1)
    coverage_outline_color:str|tuple = field(default='k')
    coverage_label_background_pad:float = field(default=1)
    coverage_label_background_linewidth:float = field(default=0)
    coverage_label_background_alpha:float = field(default=1)
    coverage_hatch_linewidth:float = field(default=0.5)

    # Default Grid Parameters
    grid_linestyle:str = field(default='--')
    grid_linewidth:float = field(default=1)
    grid_color:str|tuple = field(default='gray')

    # Default Arrow Parameters
    arrow_width:float = field(default=0.001)
    arrow_facecolor:str|tuple = field(default='k')  # If "coverage_facecolor" then the arrow's facecolor will be the color of the corresponding coverage's facecolor
    arrow_edge_color:str|tuple = field(default='k')
    arrow_linewidth:float = field(default=0)
    arrow_head_width:float = field(default=None)
    arrow_length_includes_head:bool = field(default=True)
    arrow_zorder:float = field(default=2.9)
    arrow_text_padding:float = field(default=0.05)


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


    # def make_rectangle(self,x_range,y_range,**kwargs):
    #     '''
    #     Rectangle z-order:
    #     '''

    #     x_range,y_range = self.handle_ranges(x_range,y_range)

    #     # Bottom left corner
    #     anchor_point = (x_range[0],y_range[0])

    #     width = (x_range[1] - x_range[0])

    #     height = (y_range[1] - y_range[0])

    #     if height == 0:
    #         height = self.coverage_min_rectangle_height

    #     rect_defaults = {'alpha': self.coverage_alpha,('linewidth','lw'): self.coverage_linewidth,
    #                 ('edgecolor','ec'): self.coverage_edgecolor,'label': self.coverage_label,
    #                 ('facecolor','fc'):self.coverage_color(),'coverage_outline_alpha':self.coverage_outline_alpha,
    #                 'hatch':None}

    #     alpha, linewidth, edgecolor, label, fc, coverage_outline_alpha,hatch  = extract_kwargs_with_aliases(kwargs, rect_defaults).values()

    #     rect_args = list(inspect.signature(matplotlib.patches.Rectangle).parameters)
    #     rect_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in rect_args}

    #     rect = Rectangle(anchor_point,width=width,height=height,
    #                      fc=fc,alpha=alpha,
    #                      linewidth=linewidth, edgecolor = None,
    #                      label=label,hatch=hatch,**rect_dict)
        
    #     # Set label to none
    #     rect_outline = Rectangle(anchor_point,width=width,height=height,fc=None,fill=False,alpha=coverage_outline_alpha,
    #                      linewidth=linewidth, edgecolor = edgecolor,
    #                      label=None,zorder=rect.get_zorder()+0.25,**rect_dict)
        

    #     text_args = list(inspect.signature(matplotlib.text.Text.set).parameters)+list(inspect.signature(matplotlib.text.Text).parameters)
    #     text_dict = {k: kwargs.pop(k) for k in dict(kwargs) if k in text_args}
        
    #     fontsize = text_dict.pop('fontsize',self.coverage_fontsize)
    #     label_position = kwargs.pop('label_position',rect.get_center())

    #     text = matplotlib.text.Text(*label_position,text=label,fontsize=fontsize,ha='center',va='center',zorder=5,**text_dict)
        
    #     self.patches.append([rect,rect_outline,text])

    def make_rectangle(self, x_range, y_range, **kwargs):
        """
        Creates a rectangle, its outline, and associated text, and adds them to the patches.

        Args:
            x_range (tuple): The x-coordinate range for the rectangle.
            y_range (tuple): The y-coordinate range for the rectangle.
            **kwargs: Additional keyword arguments to customize the rectangle and text.
        """
        x_range, y_range = self.handle_ranges(x_range, y_range)

        # Define bottom-left corner, width, and height
        anchor_point = (x_range[0], y_range[0])
        width = x_range[1] - x_range[0]
        height = y_range[1] - y_range[0]
        if height == 0:
            height = self.coverage_min_rectangle_height

        # Default parameters for the rectangle
        rect_defaults = {
            'alpha': self.coverage_alpha,
            ('linewidth', 'lw'): self.coverage_linewidth,
            ('edgecolor', 'ec'): self.coverage_edgecolor,
            'label': self.coverage_label,
            ('facecolor', 'fc'): self.coverage_color(),
            'coverage_outline_alpha': self.coverage_outline_alpha,
            'hatch': None
        }

        # Extract required values and manage kwargs
        alpha, linewidth, edgecolor, label, fc, coverage_outline_alpha, hatch = \
            extract_kwargs_with_aliases(kwargs, rect_defaults).values()

        # Font size and label position for the text
        fontsize = kwargs.pop('fontsize', self.coverage_fontsize)
        label_position = kwargs.pop('label_position', (anchor_point[0] + width / 2, anchor_point[1] + height / 2))

        # Create Coverage instance
        annotated_rect = Coverage.create(
            anchor_point, width, height, label,
            alpha, linewidth, edgecolor, fc, coverage_outline_alpha,
            hatch, fontsize, label_position, **kwargs
        )

        # Append to the patches list
        self.patches.extend([annotated_rect])




    # def format_coverage_label(self,text:matplotlib.text.Text,rect:Rectangle):
    #     text.set_bbox(dict(facecolor=rect.get_facecolor(),pad=self.coverage_label_background_pad,
    #                        linewidth=self.coverage_label_background_linewidth,alpha=self.coverage_label_background_alpha))

    
    # def calculate_arrow_length(self,rect:Rectangle,text_left,text_right):
    #     rect_bbox = self.ax.transData.inverted().transform(rect.get_window_extent())

    #     rect_left, rect_bottom = rect_bbox[0]
    #     rect_right, rect_top = rect_bbox[1]

    #     left_arrow_length = rect_left-text_left-0.01
    #     right_arrow_length = rect_right-text_right-0.01

    #     return left_arrow_length,right_arrow_length


    # def add_range_arrows(self,text:matplotlib.text.Text,rect:Rectangle,**arrow_kwargs):

    #     defaults = {'arrow_width': self.arrow_width,
    #                 'arrow_facecolor': self.arrow_facecolor,
    #                 'arrow_head_width': self.arrow_head_width,
    #                 'arrow_length_includes_head':self.arrow_length_includes_head,
    #                 'arrow_zorder':self.arrow_zorder,
    #                 'arrow_edge_color':self.arrow_edge_color,
    #                 'arrow_linewidth':self.arrow_linewidth}

    #     arrow_width,arrow_facecolor,arrow_head_width,arrow_length_includes_head,arrow_zorder,arrow_edge_color,arrow_linewidth = extract_kwargs_with_aliases(arrow_kwargs, defaults).values()

    #     if arrow_facecolor=='coverage_facecolor':
    #         arrow_facecolor = rect.get_facecolor()

    #     text_bbox = self.ax.transData.inverted().transform(text.get_window_extent())

    #     # Calculate the left and right bounds of the text in data coordinates
    #     text_left, text_bottom = text_bbox[0]
    #     text_right, text_top = text_bbox[1]
    #     text_y_center = (text_bottom + text_top) / 2  # The vertical center of the text

    #     arrow_props = {'width': arrow_width, 'facecolor': arrow_facecolor,'head_width':arrow_head_width,
    #                    "length_includes_head":arrow_length_includes_head,'zorder':arrow_zorder,
    #                    'edgecolor':arrow_edge_color,'linewidth':arrow_linewidth}

    #     left_arrow_length,right_arrow_length = (self.calculate_arrow_length(rect,text_left=text_left,text_right=text_right))

    #     left_arrow_left_bound = text_left - (self.arrow_text_padding-0.03)  # Subtract a bit because arrow spills over a bit further than expected
    #     left_arrow_right_bound = left_arrow_length + self.arrow_text_padding

    #     right_arrow_left_bound = text_right + self.arrow_text_padding
    #     right_arrow_right_bound = right_arrow_length - self.arrow_text_padding

    #     left_arrow = FancyArrow(left_arrow_left_bound, text_y_center, left_arrow_right_bound, 0, **arrow_props)
    #     right_arrow = FancyArrow(right_arrow_left_bound, text_y_center, right_arrow_right_bound, 0, **arrow_props)

    #     self.ax.add_artist(left_arrow)
    #     self.ax.add_artist(right_arrow)


    def add_hlines(self,y_values,**kwargs):
        zorder = kwargs.pop('zorder',1.15)
        for y_value in y_values:
            self.ax.axhline(y_value,zorder=zorder,**kwargs)

    def add_vlines(self,x_values,**kwargs):
        zorder = kwargs.pop('zorder',1.15)
        for x_value in x_values:
            self.ax.axvline(x_value,zorder=zorder,**kwargs)

    def add_grid(self,show_grid,grid_kwargs):
        if show_grid:
            defaults = {('linewidth','lw'): self.grid_linewidth,
                        ('color','c'): self.grid_color,('linestyle','ls'): self.grid_linestyle}

            linewidth, color, linestyle  = extract_kwargs_with_aliases(grid_kwargs, defaults).values()
            n_hlines = len(self.y_labels)
            n_vlines = len(self.x_labels)
            self.add_hlines(np.arange(-0.5,n_hlines+0.5,1),linewidth=linewidth,ls=linestyle,color=color)
            self.add_vlines(np.arange(0,n_vlines+1,1),linewidth=linewidth,ls=linestyle,color=color)


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


    def draw_rectangles_with_hatching(self):
        """Convert rectangles' representation to be hatches instead of a solid color"""
        rectangles = [rect for rect in self.ax.patches if isinstance(rect, Rectangle)]

        rectangle_labels = {rect.get_label() for rect in rectangles}

        rectangle_colors = [rect.get_facecolor() for rect in rectangles]

        hatch_styles = ['/', '\\', '|', '-', 'o', 'O', '.',
        '//', '\\\\', '||', '--', '++', 'xx', 'oo', 'OO', '..',
        '/o', '\\|', '|*', '-\\', '+o', 'x*', 'o-', 'O|', 'O.', '*-']  # List of hatching styles

        label_to_color = {key:value for key,value in zip(rectangle_labels,rectangle_colors)}

        color_to_hatch = {key:value for key,value in zip(set(rectangle_colors),hatch_styles)}


        matplotlib.rcParams['hatch.linewidth'] = self.coverage_hatch_linewidth

        for idx,rect in enumerate(rectangles):
            rect_label = rect.get_label()
            if rect_label is not None:
                if rect.get_hatch():
                    continue
                rect_fc = rect.get_facecolor()
                rect.set_facecolor('none')
                rect.set_hatch(color_to_hatch[rect_fc])
                rect.set_edgecolor(rect_fc)
                rect.set_linewidth(self.coverage_hatch_linewidth)

    def plot(self,with_hatches:bool=False):
        '''
        Only call after you have added all of your coverages
        '''
        self.set_up_plot()  
        self.init_coverages()
        for annotated_rect in self.patches:
            rect_outline = annotated_rect.rect_outline
            text = annotated_rect.text
            rect = annotated_rect.rect

            self.ax.add_patch(rect)
            self.ax.add_patch(rect_outline)
            text = self.ax.add_artist(text)

            self.ax.add_artist(annotated_rect.left_arrow)
            self.ax.add_artist(annotated_rect.right_arrow)

            # self.format_coverage_label(text=text,rect=rect)
            # self.add_range_arrows(text=text,rect=rect)

        if with_hatches:
            self.draw_rectangles_with_hatching()

