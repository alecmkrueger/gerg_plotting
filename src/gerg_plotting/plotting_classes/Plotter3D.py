from attrs import define
import numpy as np
import mayavi

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    instrument: SpatialInstrument

    def __attrs_post_init__(self):
        self.init_figure()

    def init_figure(self):
        raise NotImplementedError('Need to add method for initializing the mayavi figure')