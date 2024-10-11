from attrs import define,field
import numpy as np
import mayavi as mlab

from gerg_plotting.plotting_classes.Plotter3D import Plotter3D

@define
class Scatter3D(Plotter3D):

    def plot(self,var:str|None=None,point_size:int|float=0.05):
        if not self.instrument._has_var(var):
            raise ValueError(f'Instrument does not have {var}')
        if var is None:
            points = mlab.points3d(self.instrument.lon.data,self.instrument.lat.data,self.instrument.depth.data,
                        mode='sphere',resolution=8,line_width=0,scale_factor=point_size)  
        elif isinstance(var,str):  
            points = mlab.points3d(self.instrument.lon.data,self.instrument.lat.data,self.instrument.depth.data,self.instrument[var].data,
                        mode='sphere',resolution=8,line_width=0,scale_factor=point_size,vmax=self.instrument.vmax,vmin=self.instrument.vmin)
        else:
            raise ValueError(f'var must be either None or one of {self.instrument}')
        raise NotImplementedError('Add method for plotting the 3D data using Mayavi')
    
