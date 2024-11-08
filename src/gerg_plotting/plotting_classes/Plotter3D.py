from attrs import define,asdict,field
from pprint import pformat
import numpy as np
import mayavi.core.scene
import mayavi.mlab as mlab

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument,Bathy


@define
class Plotter3D:
    '''Wrapper around Mayavi'''
    data: SpatialInstrument

    bathy: Bathy = field(default=None)

    fig:mayavi.core.scene.Scene = field(default=None)
    figsize:tuple = field(default=(1920,1080))

    def init_figure(self,fig=None):
        if fig is None:
            fig = mlab.figure(size=self.figsize)
        elif isinstance(fig,mayavi.core.scene.Scene):
            fig = fig
        else:
            ValueError(f"fig must be either None or a mayavi.core.secne.Scene object")
        return fig
    
    def _has_var(self, key) -> bool:
        '''Check if object has var'''
        return key in asdict(self).keys()
    
    def _get_vars(self) -> list:
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
        raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")  

    def __setitem__(self, key, value):
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")

    def __repr__(self):
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)

    
    def convert_colormap(self, colormap, over_color=None, under_color=None) -> np.ndarray:
        """
        Converts a colormap to an array of colors scaled to 0-255 (uint8) format, with optional customization
        of the first (under_color) and last (over_color) colors in the array.

        Parameters:
            colormap (Callable): A callable that generates colors, usually a Matplotlib colormap function.
            over_color (tuple, optional): A color to assign to the highest value in the colormap (e.g., (255, 0, 0) for red).
            under_color (tuple, optional): A color to assign to the lowest value in the colormap.

        Returns:
            np.ndarray: An array of colors where each entry is a color in RGBA format (scaled to 0-255) as uint8.
        """
        # Create the colormap array by iterating over 256 color points
        colormap_array = np.array([colormap(i) for i in range(256)])
        # Scale color values from [0,1] range to [0,255] for uint8 compatibility
        colormap_array *= 255
        # Convert color array to uint8 for compatibility with visualization libraries
        colormap_array = colormap_array.astype(np.uint8)

        # Apply the under_color if specified, replacing the lowest color
        if under_color is not None:
            colormap_array[0] = under_color

        # Apply the over_color if specified, replacing the highest color
        if over_color is not None:
            colormap_array[-1] = over_color

        return colormap_array


    def format_colorbar(self,colorbar,x_pos1_offset,y_pos1_offset,x_pos2_offset,y_pos2_offset):
        """
        Formats a colorbar to adapt font sizes and colors based on frame height, improving readability and aesthetics.

        Parameters:
            colorbar (mayavi.modules.scalarbar.ScalarBar): The colorbar object to be formatted.
        """
        # Calculate font size based on frame height for adaptive scaling
        fontsize = round(((self.figsize[1] / 400) ** 1.8) + 11)
        fontcolor = (0, 0, 0)  # Set text color to black

        # Enable dynamic font scaling
        colorbar.scalar_bar.unconstrained_font_size = True

        # Set label text font size and color
        colorbar.scalar_bar.label_text_property.font_size = fontsize
        colorbar.scalar_bar.label_text_property.color = fontcolor

        # Set title text font size, color, and alignment properties
        colorbar.title_text_property.font_size = fontsize
        colorbar.title_text_property.color = fontcolor
        colorbar.title_text_property.line_offset = -7  # Adjust offset for better alignment
        colorbar.title_text_property.line_spacing = 10
        colorbar.title_text_property.vertical_justification = 'top'

        # Adjust colorbar's size and position slightly for aesthetic refinement
        if x_pos1_offset is not None or y_pos1_offset is not None:  # Check if an offset is provided
            pos1 = colorbar.scalar_bar_representation.position
            colorbar.scalar_bar_representation.position = [pos1[0] + x_pos1_offset, pos1[1] + y_pos1_offset]

        if x_pos2_offset is not None or y_pos2_offset is not None:  # Check if an offset is provided
            pos2 = colorbar.scalar_bar_representation.position2
            colorbar.scalar_bar_representation.position2 = [pos2[0] + x_pos2_offset, pos2[1] + y_pos2_offset]


    def add_colorbar(self, mappable, cmap_title,over_color=None,x_pos1_offset=None,y_pos1_offset=None,x_pos2_offset=None,y_pos2_offset=None,cmap=None):
        """
        Adds a colormap to a 3D point cloud plot and attaches a formatted vertical colorbar with a title.

        Parameters:
            points (mayavi.modules.glyph.Glyph): The 3D points to which the colormap will be applied.
            cmap_title (str): Title for the colorbar, indicating the variable represented by the colors.
            cmap (Callable, optional): A colormap function to use. If None, the default colormap is applied.
        """
        # Apply custom colormap if provided, converting to compatible color format
        if cmap is not None:
            mappable.module_manager.scalar_lut_manager.lut.table = self.convert_colormap(cmap,over_color=over_color)

        # Add a colorbar with custom title, label format, and vertical orientation
        colorbar = mlab.colorbar(mappable, orientation='vertical', title=cmap_title, label_fmt='%0.1f', nb_labels=6)
        colorbar.scalar_bar_representation.proportional_resize = True  # Enable proportional resizing

        # Format the colorbar for improved readability and consistency
        self.format_colorbar(colorbar,
                             x_pos1_offset=x_pos1_offset,y_pos1_offset=y_pos1_offset,
                             x_pos2_offset=x_pos2_offset, y_pos2_offset=y_pos2_offset)


