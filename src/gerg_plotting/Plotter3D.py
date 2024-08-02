from attrs import define
import numpy as np
from gerg_plotting.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    instrument: SpatialInstrument