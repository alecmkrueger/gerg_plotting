from attrs import define,field,asdict
from matplotlib.colors import Colormap
import numpy as np
from pprint import pformat
from datetime import datetime

from gerg_plotting.modules.validations import is_flat_numpy_array
from gerg_plotting.modules.utilities import to_numpy_array


@define
class Variable():
    """
    A class representing a scientific variable with its values and visualization properties.

    This class handles values arrays along with their metadata and visualization settings,
    providing methods for values access and label generation.

    Parameters
    ----------
    values : np.ndarray
        The numerical values for the variable
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
    values : np.ndarray
        Flat numpy array containing the variable values
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
    values: np.ndarray = field(converter=to_numpy_array, validator=is_flat_numpy_array)
    name: str
    cmap: Colormap = field(default=None)
    units: str = field(default=None)
    _vmin: float = field(default=None)
    _vmax: float = field(default=None)
    _label: str = field(default=None)
    
    @property
    def attrs(self) -> list:
        """List of all attributes for the variable."""
        return list(asdict(self).keys())

    @property
    def label(self) -> str:
        """Formatted label including variable name and units if available."""
        if self._label is None:
            unit = f" ({self.units})" if self.units is not None else ''
            name = self.name.replace('_',' ').title()
            self._label = f"{name}{unit}"
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        """Set custom label for the variable."""
        self._label = value

    @property
    def vmin(self) -> float:
        """Minimum value for visualization, using 1st percentile for numeric data."""
        if self._vmin is None:
            valid_types = np.typecodes['AllFloat'] + np.typecodes['AllInteger']
            if self.values.dtype.kind in valid_types:
                self._vmin = np.nanmin(self.values)
        return self._vmin

    @vmin.setter
    def vmin(self, value: float) -> None:
        """Set minimum value for visualization."""
        self._vmin = value

    @property
    def vmax(self) -> float:
        """Maximum value for visualization"""
        if self._vmax is None:
            valid_types = np.typecodes['AllFloat'] + np.typecodes['AllInteger']
            if self.values.dtype.kind in valid_types:
                self._vmax = np.nanmax(self.values)
        return self._vmax

    @vmax.setter
    def vmax(self, value: float) -> None:
        """Set maximum value for visualization."""
        self._vmax = value


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
        # Get all attributes except values
        attrs = self.get_attrs()
        attrs.remove('values')
        
        # Calculate width needed for values column
        sample_values = [self._format_value(x) for x in self.values[:5]]
        max_values_width = max(len(str(x)) for x in sample_values) if sample_values else 0
        # Add padding and constrain between min and max values
        values_width = min(max(max_values_width * 8, 100), 200)  # Min 100px, Max 200px
        
        html = f'<td style="padding:0 0px;vertical-align:top">'
        html += f'<table style="table-layout:fixed;width:{values_width + 90}px"><tbody>'
        
        # Add subheaders
        html += f'''
        <tr>
            <th style="width:80px;padding:0;text-align:center;border-bottom:1px solid #ddd">Attribute</th>
            <th style="width:{values_width}px;padding:0;text-align:center;border-bottom:1px solid #ddd">Value</th>
        </tr>
        '''
        
        # Add attributes in two columns with dynamic width
        for attr in attrs:
            value = getattr(self, attr)
            html += f'''
            <tr>
                <td style="padding-right:10px;width:80px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><strong>{attr}</strong></td>
                <td style="text-align:center;width:{values_width}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{self._format_value(value)}</td>
            </tr>
            '''
        
        html += f'''<tr><td colspan="2" style="text-align:center"><strong>Data</strong></td></tr>'''
        
        # Add values values with indices
        for i in range(min(5, len(self.values))):
            html += f'''
            <tr>
                <td style="padding-right:10px;width:80px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"><strong>{i}</strong></td>
                <td style="text-align:left;width:{values_width}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{self._format_value(self.values[i])}</td>
            </tr>
            '''
        
        html += f'<tr><td colspan="2">... Length: {len(self.values)}</td></tr>'
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
    