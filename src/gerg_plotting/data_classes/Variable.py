from attrs import define,field,asdict
from matplotlib.colors import Colormap
from typing import Iterable
import numpy as np
from pprint import pformat

from gerg_plotting.modules.validations import is_flat_numpy_array
from gerg_plotting.modules.utilities import to_numpy_array


@define
class Variable():
    data:Iterable = field(converter=to_numpy_array,validator=is_flat_numpy_array)
    name:str
    cmap:Colormap = field(default=None)
    units:str = field(default=None)  # Turn off units by passing/assigning to None
    vmin:float = field(default=None)
    vmax:float = field(default=None)
    label:str = field(default=None)  # Set label to be used on figure and axes, use if desired

    def __attrs_post_init__(self):
        self.get_vmin_vmax()

    def _has_var(self, key):
        return key in asdict(self).keys()
    def __getitem__(self, key):
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Attribute '{key}' not found")
    def __setitem__(self, key, value):
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)

    def get_attrs(self):
        return list(asdict(self).keys())
    
    def get_vmin_vmax(self):
        if self.name != 'time':  # do not calcluate vmin and vmax for time
            if self.vmin is None:
                self.vmin = np.nanmin(self.data)
            if self.vmax is None:
                self.vmax = np.nanmax(self.data)

    def get_label(self):
        '''Assign the label if it was not passed'''
        if self.label is None:
            # Define the units that are added to the label
            # if the units are defined, we will use them, else it will be an empty string
            unit = f" ({self.units})" if self.units is not None else ''
            # The label is created from the name of the variable with the units
            self.label = f"{self.name.capitalize()}{unit}"
        return self.label