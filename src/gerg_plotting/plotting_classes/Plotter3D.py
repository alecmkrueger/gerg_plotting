from attrs import define,asdict,field
from pprint import pformat
import numpy as np
import mayavi.mlab as mlab

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    instrument: SpatialInstrument

    def __attrs_post_init__(self):
        self.init_figure()

    def init_figure(self):
        fig = mlab.figure()
        # raise NotImplementedError('Need to add method for initializing the mayavi figure')
    
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
