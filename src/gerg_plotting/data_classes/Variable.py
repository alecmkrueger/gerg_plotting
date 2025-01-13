from attrs import define,field,asdict
from matplotlib.colors import Colormap
from typing import Iterable
import numpy as np
from pprint import pformat
from datetime import datetime

from gerg_plotting.modules.validations import is_flat_numpy_array
from gerg_plotting.modules.utilities import to_numpy_array


@define
class Variable():
    """
    A class representing a scientific variable with its data and visualization properties.

    This class handles data arrays along with their metadata and visualization settings,
    providing methods for data access and label generation.

    Parameters
    ----------
    data : np.ndarray
        The numerical data for the variable
    name : str
        Name identifier for the variable
    cmap : Colormap, optional
        Matplotlib colormap for visualization
    units : str, optional
        Units of measurement
    vmin : float, optional
        Minimum value for visualization scaling
    vmax : float, optional
        Maximum value for visualization scaling
    label : str, optional
        Custom label for plotting

    Attributes
    ----------
    data : np.ndarray
        Flat numpy array containing the variable data
    name : str
        Variable name identifier
    cmap : Colormap
        Colormap for visualization
    units : str
        Units of measurement
    vmin : float
        Minimum value for visualization
    vmax : float
        Maximum value for visualization
    label : str
        Display label for plots
    """
    data:np.ndarray = field(converter=to_numpy_array,validator=is_flat_numpy_array)
    name:str
    cmap:Colormap = field(default=None)
    units:str = field(default=None)  # Turn off units by passing/assigning to None
    vmin:float = field(default=None)
    vmax:float = field(default=None)
    label:str = field(default=None)  # Set label to be used on figure and axes, use if desired


    def __attrs_post_init__(self) -> None:
        """Inittializes vmin and vmax if not set"""
        self.get_vmin_vmax()


    def _has_var(self, key):
        """
        Check if an attribute exists.

        Parameters
        ----------
        key : str
            Attribute name to check

        Returns
        -------
        bool
            True if attribute exists
        """
        return key in asdict(self).keys()
    

    def __getitem__(self, key):
        """Get an attribute by key."""
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Attribute '{key}' not found")
    

    def __setitem__(self, key, value) -> None:
        """Set an attribute by key."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")

    def _format_value(self,value):
        if isinstance(value, float):
            return f"{value:.6f}"
        elif isinstance(value, np.datetime64):
            value = value.astype('M8[ms]').astype(datetime)
            return f"{value:%y-%m-%d %H:%M:%S}"
        elif isinstance(value, datetime):
            return f"{value:%y-%m-%d %H:%M:%S}"
        elif isinstance(value,Colormap):
            return f"{value.name}"
        else:
            return str(value)
                    
    def _repr_html_(self) -> str:
        # Get all attributes except data
        attrs = self.get_attrs()
        attrs.remove('data')
        
        # Calculate width needed for data column
        sample_data = [self._format_value(x) for x in self.data[:5]]
        max_data_width = max(len(str(x)) for x in sample_data) if sample_data else 0
        # Add padding and constrain between min and max values
        data_width = min(max(max_data_width * 8, 100), 200)  # Min 100px, Max 200px
        
        html = f'<td style="padding:0 0px;vertical-align:top">'
        html += f'<table style="table-layout:fixed;width:{data_width + 90}px"><tbody>'
        
        # Add subheaders
        html += f'''
        <tr>
            <th style="width:80px;padding:0;text-align:center;border-bottom:1px solid #ddd">Attribute</th>
            <th style="width:{data_width}px;padding:0;text-align:center;border-bottom:1px solid #ddd">Value</th>
        </tr>
        '''
        
        # Add attributes in two columns with dynamic width
        for attr in attrs:
            value = getattr(self, attr)
            html += f'''
            <tr>
                <td style="padding-right:10px;width:80px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><strong>{attr}</strong></td>
                <td style="text-align:center;width:{data_width}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{self._format_value(value)}</td>
            </tr>
            '''
        
        html += f'''<tr><td colspan="2" style="text-align:center"><strong>Data</strong></td></tr>'''
        
        # Add data values with indices
        for i in range(min(5, len(self.data))):
            html += f'''
            <tr>
                <td style="padding-right:10px;width:80px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><strong>{i}</strong></td>
                <td style="text-align:left;width:{data_width}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{self._format_value(self.data[i])}</td>
            </tr>
            '''
        
        html += f'<tr><td colspan="2">... Length: {len(self.data)}</td></tr>'
        html += '</tbody></table></td>'
        
        return html



    def __repr__(self) -> None:
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)


    def get_attrs(self) -> list:
        """
        Get list of all attributes for the variable.

        Returns
        -------
        list
            List of attribute names
        """
        return list(asdict(self).keys())
    

    def get_vmin_vmax(self,ignore_existing:bool=False) -> None:
        """
        Calculate or update the minimum and maximum values for visualization.

        Uses 1st and 99th percentiles of the data to set visualization bounds,
        excluding time variables.

        Parameters
        ----------
        ignore_existing : bool, optional
            If True, recalculate bounds even if they exist
        """
        if self.name != 'time':  # do not calculate vmin and vmax for time
            if self.vmin is None or ignore_existing:
                self.vmin = np.nanpercentile(self.data, 1)  # 1st percentile (lower 1%)
            if self.vmax is None or ignore_existing:
                self.vmax = np.nanpercentile(self.data, 99)  # 99th percentile (upper 1%)

    def reset_label(self) -> None:
        """Reset the label to the variable name."""
        self.label = None

    def get_label(self) -> str:
        """
        Generate a formatted label for the variable.

        Returns
        -------
        str
            Formatted label including variable name and units if available
        """
        if self.label is None:
            # Define the units that are added to the label
            # if the units are defined, we will use them, else it will be an empty string
            unit = f" ({self.units})" if self.units is not None else ''
            # Replace any underscores in the name with spaces then capitalize them
            name = self.name.replace('_',' ').title()
            # The label is created from the name of the variable with the units
            self.label = f"{name}{unit}"
        return self.label