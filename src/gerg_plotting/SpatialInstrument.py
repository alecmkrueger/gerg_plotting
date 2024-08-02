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

    def has_var(self, key):
        return key in asdict(self).keys()
    def __getitem__(self, key):
        if self.has_var(key):
            return getattr(self, key)
        raise KeyError(f"Attribute '{key}' not found")
    def __setitem__(self, key, value):
        if self.has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)