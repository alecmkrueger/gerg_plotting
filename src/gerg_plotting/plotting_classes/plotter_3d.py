from attrs import define, asdict, field
from pprint import pformat
import numpy as np
import pyvista as pv

from gerg_plotting.data_classes.data import Data
from gerg_plotting.data_classes.bathy import Bathy
from gerg_plotting.modules.calculations import get_center_of_mass


@define
class Plotter3D:

    data: Data
    bathy: Bathy = field(default=None)
    plotter: pv.Plotter = field(default=None)
    figsize: tuple = field(default=(1920, 1080))

    def _has_var(self, key) -> bool:
        """
        Check for existence of attribute.

        Parameters
        ----------
        key : str
            Attribute name to check

        Returns
        -------
        bool
            True if attribute exists, False otherwise
        """
        # Check if key exists in the object's dictionary representation
        return key in asdict(self).keys()

    def get_vars(self) -> list:
        """
        Get list of object attributes.

        Returns
        -------
        list
            List of attribute names
        """
        # Get list of attributes by converting object to dictionary
        return list(asdict(self).keys())
    
    def _check_var(self, var) -> None:
        """
        Verify variable exists in data object.

        Parameters
        ----------
        var : str or None
            Variable name to check

        Raises
        ------
        ValueError
            If variable doesn't exist in data
        """
        # Proceed only if a variable is specified
        if var is not None:
            # Verify if the variable exists in the data, raise error if not
            if not self.data._has_var(var):
                raise ValueError(f'Instrument does not have {var}')

    def __getitem__(self, key: str):
        """
        Access class attributes using dictionary-style indexing.

        Args:
            key (str): The attribute name to access.

        Returns:
            The value of the specified attribute.
        """
        # Check for existence of the attribute
        if self._has_var(key):
            return getattr(self, key)  # Return attribute value if found
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")  

    def __setitem__(self, key, value):
        """
        Set class attributes using dictionary-style indexing.

        Args:
            key (str): The attribute name to set.
            value: The value to assign to the attribute.
        """
        # Check for existence of the attribute
        if self._has_var(key):
            setattr(self, key, value)  # Set attribute value if found
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")

    def __repr__(self) -> None:
        """
        Pretty-print the class attributes for improved readability.

        Returns:
            str: A formatted string representation of the object.
        """
        # Convert attributes to formatted string for display
        return pformat(asdict(self), width=1)
    
    def init_figure(self):
        self.plotter = pv.Plotter(off_screen=False, window_size=self.figsize)
        
    def _pre_show(self):
        self.plotter.set_scale(zscale=self.data.bounds.vertical_scalar)
        # Set Focus last right before show
        self.plotter.set_focus(get_center_of_mass(lon=self.data.lon.values,
                                                lat=self.data.lat.values,
                                                pressure=self.data.depth.values*self.data.bounds.vertical_scalar))

    def show(self,**kwargs):
        self._pre_show()
        self.plotter.show(**kwargs)
        
    def export_html(self, filename):
        self._pre_show()
        self.plotter.export_html(filename)
    
        
    def close(self):
        raise NotImplementedError

    def save(self,filename,**kwargs):
        raise NotImplementedError

    def convert_colormap(self, colormap, over_color=None, under_color=None) -> np.ndarray:
        """
        Convert colormap to uint8 color array.

        Parameters
        ----------
        colormap : Callable
            Function generating colors (matplotlib colormap)
        over_color : tuple, optional
            Color for highest value
        under_color : tuple, optional
            Color for lowest value

        Returns
        -------
        np.ndarray
            Array of RGBA colors scaled to 0-255
        """
        # Create color array by evaluating colormap across 256 points
        colormap_array = np.array([colormap(i) for i in range(256)])
        colormap_array *= 255  # Scale colors to [0, 255] range for uint8 compatibility
        colormap_array = colormap_array.astype(np.uint8)  # Convert to uint8 for visualization libraries

        # Apply under_color if provided, replacing the first color in the array
        if under_color is not None:
            colormap_array[0] = under_color

        # Apply over_color if provided, replacing the last color in the array
        if over_color is not None:
            colormap_array[-1] = over_color

        return colormap_array

    def add_colorbar(self,**kwargs):
        self.plotter.add_scalar_bar(**kwargs)


