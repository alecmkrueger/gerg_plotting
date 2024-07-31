from attrs import define
import numpy as np


@define
class Plotter3D:
    x:np.ndarray
    y:np.ndarray
    z:np.ndarray