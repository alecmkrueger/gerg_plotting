from attrs import define, field
import cmocean
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pyvista as pv

from pathlib import Path

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
        self.init_figure()
        # Ensure that the points data is in (n_points by 3) format
        points = self.make_points_3d(x, y, z)
        scatter_points = pv.PolyData(points)
        # Add color data if provided
        if var is not None:
            color_label = self.data[var].get_label()
            scatter_points[color_label] = self.data[var].values
            cmap = self.data[var].cmap
        else:
            color_label = None
            cmap = None
        # Add the mesh to the plotter
        self.plotter.add_mesh(scatter_points, scalars=color_label, show_scalar_bar=False, cmap = cmap,render_points_as_spheres=True, point_size=10)
        if color_label is not None:
            self.add_colorbar(title=color_label, height=0.5, vertical=True, position_x=0.025, position_y=0.04,fmt="%.1f")

    def add_bathy(self):
        # Get bathymetry data
        seafloor_data_path = Path(__file__).parent.parent.joinpath('seafloor_data/gom_srtm30_plus.txt')
        df = pd.read_csv(seafloor_data_path,sep='\t')

        # Flip z data
        df['z'] = df['z']*-1

        # Filter the data to the bounds of the data
        filtered_df = df[
            (df['long'] >= self.data.bounds.lon_min) & 
            (df['long'] <= self.data.bounds.lon_max) & 
            (df['lat'] >= self.data.bounds.lat_min) & 
            (df['lat'] <= self.data.bounds.lat_max)
        ]

        coords = filtered_df.values

        # Make the structured surface manually
        structured = pv.StructuredGrid()
        # Set coordinates
        structured.points = coords
        # Set the dimensions of the structured grid
        structured.dimensions = [len(filtered_df.long.unique()), len(filtered_df.lat.unique()), 1]

        # Apply an Elevation filter
        elevation = structured.elevation()

        # Adjust the colormap
        cmap = cmocean.tools.crop_by_percent(matplotlib.colormaps.get_cmap('Blues'), 10, 'min')
        # Set the under color (land color) for the colormap
        land_color = [231 / 255, 194 / 255, 139 / 255]
        cmap.set_under(land_color)
        color_label = f'Depth ({self.data.bounds.vertical_units})'
        elevation[color_label] = elevation.points[:, 2]
        
        annotations = {self.data.depth.values.min(): 'Glider/nMax/nDepth'}
        self.plotter.add_mesh(elevation, scalars='Depth (m)',show_scalar_bar=False,cmap=cmap, show_edges=False,below_color=land_color,
                              clim=(0,filtered_df.z.max()),flip_scalars=False, lighting=True,annotations=annotations)
        
        
        self.add_colorbar(title='Depth (m)', width=0.5, vertical=False, below_label='', fmt="%.1f")


    def map(self, var: str | None = None) -> None:
        self.init_figure()
        x = 'lon'
        y = 'lat'
        z = 'depth'
        self.scatter(x, y, z, var)
        self.add_bathy()
        
