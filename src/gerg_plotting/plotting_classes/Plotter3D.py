from attrs import define,asdict,field
from pprint import pformat
import numpy as np
import mayavi.core.scene
import mayavi.mlab as mlab

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    '''Wrapper around Mayavi'''
    data: SpatialInstrument

    def init_figure(self,fig=None,figsize=(1920,1080)):
        if fig is None:
            fig = mlab.figure(size=figsize)
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
    
import numpy as np
from mayavi import mlab

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


def format_colorbar(colorbar, frame_height=1080):
    """
    Formats a colorbar to adapt font sizes and colors based on frame height, improving readability and aesthetics.

    Parameters:
        colorbar (mayavi.modules.scalarbar.ScalarBar): The colorbar object to be formatted.
        frame_height (int, optional): The height of the display frame, used to scale font sizes. Default is 1080.
    """
    # Calculate font size based on frame height for adaptive scaling
    fontsize = round(((frame_height / 400) ** 1.8) + 11)
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
    pos2 = colorbar.scalar_bar_representation.position2
    colorbar.scalar_bar_representation.position2 = [pos2[0] - 0.02, pos2[1] - 0.01]


def add_colormap(self, points, cmap_title, cmap=None):
    """
    Adds a colormap to a 3D point cloud plot and attaches a formatted vertical colorbar with a title.

    Parameters:
        points (mayavi.modules.glyph.Glyph): The 3D points to which the colormap will be applied.
        cmap_title (str): Title for the colorbar, indicating the variable represented by the colors.
        cmap (Callable, optional): A colormap function to use. If None, the default colormap is applied.
    """
    # Apply custom colormap if provided, converting to compatible color format
    if cmap is not None:
        points.module_manager.scalar_lut_manager.lut.table = self.convert_colormap(cmap)

    # Add a colorbar with custom title, label format, and vertical orientation
    var_colorbar = mlab.colorbar(points, orientation='vertical', title=cmap_title, label_fmt='%0.1f', nb_labels=6)
    var_colorbar.scalar_bar_representation.proportional_resize = True  # Enable proportional resizing

    # Format the colorbar for improved readability and consistency
    self.format_colorbar(var_colorbar, frame_height=self.settings.figsize[1])

    # Adjust colorbar position slightly for better layout alignment
    pos2 = var_colorbar.scalar_bar_representation.position2
    var_colorbar.scalar_bar_representation.position2 = [pos2[0] - 0.02, pos2[1] - 0.01]

