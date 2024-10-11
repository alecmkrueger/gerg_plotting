from attrs import define,field,asdict
from pprint import pformat
from typing import Iterable
import cmocean

from gerg_plotting.NonSpatialInstruments import Variable


@define(slots=False)
class SpatialInstrument:
    # Dims
    lat: Iterable|Variable|None = field(default=None)
    lon: Iterable|Variable|None = field(default=None)
    depth: Iterable|Variable|None = field(default=None)
    time: Iterable|Variable|None = field(default=None)
    
    # Custom variables dictionary to hold dynamically added variables
    custom_variables: dict = field(factory=dict)

    def _has_var(self, key):
        return key in asdict(self).keys() or key in self.custom_variables

    def __getitem__(self, key):
        """Allows accessing standard and custom variables via indexing."""
        if self._has_var(key):
            return getattr(self, key, self.custom_variables.get(key))
        raise KeyError(f"Variable '{key}' not found.")

    def __setitem__(self, key, value):
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            if key in asdict(self):
                setattr(self, key, value)
            else:
                self.custom_variables[key] = value
        else:
            raise KeyError(f"Variable '{key}' not found.")
        
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self),width=1)
    
    def _init_dims(self):
        self.init_variable(var='lat', cmap=cmocean.cm.haline, units='°', vmin=None, vmax=None)
        self.init_variable(var='lon', cmap=cmocean.cm.thermal, units='°', vmin=None, vmax=None)
        self.init_variable(var='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
        self.init_variable(var='time', cmap=cmocean.cm.thermal, units='', vmin=None, vmax=None)

    def init_variable(self, var: str, cmap, units, vmin, vmax):
        """Initializes standard variables if they are not None and of type np.ndarray."""
        if self._has_var(var):
            if self[var] is not None:
                self[var] = Variable(
                    data=self[var],
                    name=var.capitalize(),
                    cmap=cmap,
                    units=units,
                    vmin=vmin,
                    vmax=vmax
                )
        else:
            raise ValueError(f'{var.capitalize()} does not exist')

    def add_custom_variable(self, variable_name: str, variable: Variable):
        """Adds a custom Variable object and makes it accessible via both dot and dict syntax."""
        if not isinstance(variable, Variable):
            raise TypeError(f"The provided object is not an instance of the Variable class.")
        
        if hasattr(self, variable_name):
            raise AttributeError(f"The variable '{variable_name}' already exists.")
        else:
            # Add to custom_variables and dynamically create the attribute
            self.custom_variables[variable_name] = variable
            setattr(self, variable_name, variable)

