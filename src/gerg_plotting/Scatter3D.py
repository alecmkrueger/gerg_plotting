from attrs import define,field
import numpy as np
import mayavi as mlab

from gerg_plotting.Plotter3D import Plotter3D

@define
class Scatter3D(Plotter3D):

    def plot(self,var):
        if not self.instrument.has_var(var):
            raise ValueError(f'Instrument does not have {var}')
        points = mlab.points3d(self.instrument.lon,self.instrument.lat,self.instrument.depth,self.instrument[self.instrument[var]],
                    mode='sphere',resolution=8,line_width=0,scale_factor=self.settings.point_size,vmax=self.settings.vmax,vmin=self.settings.vmin)
        raise NotImplementedError('Add method for plotting the 3D data using Mayavi')
    
