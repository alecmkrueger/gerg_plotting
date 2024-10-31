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
        raise NotImplementedError('Need to add method for initializing the mayavi figure')
    
    def __getitem__(self, key: str):
        '''
        Allow dictionary-style access to class attributes.
        
        Args:
            key (str): The attribute name to access.
        
        Returns:
            The value of the specified attribute.
        '''
        return asdict(self)[key]

    def __repr__(self):
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)