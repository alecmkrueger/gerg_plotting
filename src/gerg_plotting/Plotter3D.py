from attrs import define
import numpy as np
from gerg_plotting.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    instrument: SpatialInstrument

    def init_figure(self):
        raise NotImplementedError('Need to add method for initializing the mayavi figure')