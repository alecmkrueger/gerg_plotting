from attrs import define,field
import numpy as np

from gerg_plotting.Plotter3D import Plotter3D

@define
class Scatter3D(Plotter3D):
    x:np.ndarray = field(factory=np.ndarray)
    y:np.ndarray = field(factory=np.ndarray)
    z:np.ndarray = field(factory=np.ndarray)

    def plot():
        raise NotImplementedError('Add method for plotting the 3D data using Mayavi')