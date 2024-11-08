from attrs import define,field
import mayavi.core
import mayavi.core.scene
import mayavi.modules
import mayavi.modules.axes
import numpy as np
import mayavi.mlab as mlab
import mayavi
from functools import partial
import cmocean
import matplotlib.pyplot as plt

from gerg_plotting.plotting_classes.Plotter3D import Plotter3D
from gerg_plotting.data_classes.SpatialInstruments import Bathy

@define
class ScatterPlot3D(Plotter3D):

    fig:mayavi.core.scene.Scene = field(default=None)
    figsize:tuple = field(default=(1920,1080))

    def show(self):
        mlab.show()

    def _check_var(self,var):
        if var is not None:
            if not self.data._has_var(var):
                raise ValueError(f'Instrument does not have {var}')

    def _points3d(self,var,point_size,fig,vertical_scalar):
        if vertical_scalar is not None:
            self.data['depth'].data = self.data['depth'].data/vertical_scalar
        if var is None:
            points = mlab.points3d(self.data.lon.data,self.data.lat.data,self.data.depth.data,
                        mode='sphere',resolution=8,scale_factor=point_size,figure=fig)
        elif isinstance(var,str):
            points = mlab.points3d(self.data.lon.data,self.data.lat.data,self.data.depth.data,self.data[var].data,
                        mode='sphere',resolution=8,scale_factor=point_size,vmax=self.data[var].vmax,vmin=self.data[var].vmin,figure=self.fig)
            points.glyph.scale_mode = 'scale_by_vector'
            self.add_colormap(mappable=points,cmap_title=self.data[var].get_label(),x_pos1_offset=0.04,y_pos1_offset=0,x_pos2_offset=-0.02,y_pos2_offset=0.01)
        else:
            if vertical_scalar is not None:
                self.data['depth'].data = self.data['depth'].data*vertical_scalar
            raise ValueError(f'var must be either None or one of {self.data}')
        self.data['depth'].data = self.data['depth'].data*vertical_scalar
        
    def _add_bathy(self,fig,bounds_padding,vertical_scaler=None):
        # Get bathymetry data
        # print(f'{self.data.detect_bounds(bounds_padding=bounds_padding) = }')
        bathy_class = Bathy(bounds=self.data.detect_bounds(bounds_padding=bounds_padding))
        x_bathy,y_bathy,z_bathy = bathy_class.get_bathy()

        # Rescale depth
        if vertical_scaler is not None:
            z_bathy = z_bathy/vertical_scaler
        # Plot Bathymetry data
        bathy = mlab.mesh(x_bathy,y_bathy,z_bathy,vmax=0,figure=fig)
        # Change colormap   
        land_color = [231,194,139,255]
        bathy_cmap = plt.get_cmap('Blues_r')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap,25,'max')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap,18,'min')

        self.add_colormap(mappable=bathy,cmap_title=bathy_class.get_label(),x_pos1_offset=0.04,y_pos1_offset=0,x_pos2_offset=-0.02,y_pos2_offset=0.01)

        # bathy.module_manager.scalar_lut_manager.lut.table = self.convert_colormap(bathy_cmap,over_color=land_color)
        # Add and format colorbar
        # bathy_colorbar = mlab.colorbar(bathy, orientation='vertical',title=bathy_class.get_label(),label_fmt='%0.1f',nb_labels=6)  # Add colorbar
        # bathy_colorbar.scalar_bar_representation.position = [0.89, 0.15]  # Adjust position
        # self.format_colorbar(bathy_colorbar,frame_height=self.settings.figsize[1])
        # pos1 = bathy_colorbar.scalar_bar_representation.position
        # pos2 = bathy_colorbar.scalar_bar_representation.position2
        # bathy_colorbar.scalar_bar_representation.position = [pos1[0]+0.04,pos1[1]]
        # bathy_colorbar.scalar_bar_representation.position2 = [pos2[0]-0.02,pos2[1]-0.01]


    def scatter(self,var:str|None=None,point_size:int|float=0.05,vertical_scalar=None,fig=None,show:bool=True):
        self.fig = self.init_figure(fig=fig)

        self._check_var(var=var)
            
        self._points3d(var=var,point_size=point_size,fig=fig,vertical_scalar=vertical_scalar)
            
        if show:
            self.show()

    def map(self,var:str|None=None,point_size:int|float=0.05,bounds_padding=0,vertical_scalar=None,fig=None,show:bool=True):
        self.fig = self.init_figure(fig=fig)

        self._add_bathy(fig=fig,bounds_padding=bounds_padding,vertical_scaler=vertical_scalar)
            
        self._check_var(var=var)
            
        self._points3d(var=var,point_size=point_size,fig=fig,vertical_scalar=vertical_scalar)
            
        if show:
            self.show()
    


