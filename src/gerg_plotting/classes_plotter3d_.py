from attrs import define
import numpy as np
from gerg_plotting.classes_data import SpatialData


@define
class Plotter3D:
    instrument: SpatialData