from attrs import define, field
import cmocean
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

from gerg_plotting.plotting_classes.plotter_3d import Plotter3D
from gerg_plotting.data_classes.bathy import Bathy

@define
class ScatterPlot3D(Plotter3D):

    def _add_bathy(self) -> None:
        raise NotImplementedError
    
    def make_points_3d(self,x:str,y:str,z:str) -> np.ndarray:
        """A helper to make a 3D NumPy array of points (n_points by 3)"""
        # Access the data from the Data object
        points = [[lon,lat,depth] for lon,lat,depth in zip(self.data[x].values,self.data[y].values,self.data[z].values)]
        
        return np.array(points)

    def scatter(self, x:str, y:str, z:str, var: str | None = None) -> None:
        # Ensure that the points data is in (n_points by 3) format
        points = self.make_points_3d(x, y, z)
        pv.PolyData(points)
        raise NotImplementedError

    def map(self, var: str | None = None) -> None:
        raise NotImplementedError
