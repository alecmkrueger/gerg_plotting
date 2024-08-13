from attrs import define,field,asdict
import numpy as np
from gerg_plotting.NonSpatialInstruments import CMaps,Units
from pprint import pformat


@define
class SpatialInstrument:
    # Dims
    lat:np.ndarray = field(default=None)
    lon:np.ndarray = field(default=None)
    depth:np.ndarray = field(default=None)
    time:np.ndarray = field(default=None)
    cmaps:CMaps = field(factory=CMaps)
    units:Units = field(factory=Units)
    vars_with_units:dict = field(factory=dict)

    def __attrs_post_init__(self):
        self.make_var_with_units()

    def has_var(self, key):
        return key in asdict(self).keys()
    def __getitem__(self, key):
        if self.has_var(key):
            return getattr(self, key)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __setitem__(self, key, value):
        if self.has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self),indent=1,width=2,compact=True,depth=1)
    def make_var_with_units(self):
        for key in asdict(self).keys():
            if key in asdict(self.units).keys():
                unit = self.units[key]
                if unit is not None:
                    var_with_units = f"{key} ({unit})"
                    self.vars_with_units[key] = var_with_units
                elif unit == '':
                    self.vars_with_units[key] = f'{key}'
                else:
                    continue

