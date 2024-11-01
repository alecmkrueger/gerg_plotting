from attrs import define,field
import mayavi.core
import mayavi.core.scene
import mayavi.modules
import mayavi.modules.axes
import numpy as np
import mayavi.mlab as mlab
import mayavi

from gerg_plotting.plotting_classes.Plotter3D import Plotter3D

@define
class ScatterPlot3D(Plotter3D):

    fig:mayavi.core.scene.Scene = field(default=None)
    figsize:tuple = field(default=(1920,1080))

    def show(self):
        mlab.show()

    def plot(self,var:str|None=None,point_size:int|float=0.05,fig=None,show:bool=True):
        if fig is None:
            self.fig = self.init_figure(figsize=self.figsize)
        elif isinstance(fig,mayavi.core.scene.Scene):
            self.fig = fig
        if var is not None:
            if not self.instrument._has_var(var):
                raise ValueError(f'Instrument does not have {var}')
        if var is None:
            points = mlab.points3d(self.instrument.lon.data,self.instrument.lat.data,self.instrument.depth.data,
                        mode='sphere',resolution=8,scale_factor=point_size,figure=fig)
        elif isinstance(var,str):
            points = mlab.points3d(self.instrument.lon.data,self.instrument.lat.data,self.instrument.depth.data,self.instrument[var].data,
                        mode='sphere',resolution=8,scale_factor=point_size,vmax=self.instrument[var].vmax,vmin=self.instrument[var].vmin,figure=self.fig)
            points.glyph.scale_mode = 'scale_by_vector'
        else:
            raise ValueError(f'var must be either None or one of {self.instrument}')
        
        if show:
            self.show()
    


