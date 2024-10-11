from attrs import define,field
import numpy as np
import mayavi as mlab

from gerg_plotting.Plotter3D import Plotter3D

@define
class Scatter3D(Plotter3D):

    def plot(self,var:str|None=None,point_size:int|float=0.05):
        if not self.instrument.has_var(var):
            raise ValueError(f'Instrument does not have {var}')
        if var is None:
            points = mlab.points3d(self.instrument.lon,self.instrument.lat,self.instrument.depth,
                        mode='sphere',resolution=8,line_width=0,scale_factor=point_size)  
        elif isinstance(var,str):  
            points = mlab.points3d(self.instrument.lon,self.instrument.lat,self.instrument.depth,self.instrument[self.instrument[var]],
                        mode='sphere',resolution=8,line_width=0,scale_factor=point_size,vmax=self.settings.vmax,vmin=self.settings.vmin)
        else:
            raise ValueError(f'var must be either None or one of {self.instrument.vars}')
        raise NotImplementedError('Add method for plotting the 3D data using Mayavi')
    
