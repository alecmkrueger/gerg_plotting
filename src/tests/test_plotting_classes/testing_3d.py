# from gerg_plotting import data_from_netcdf,Data,cmocean
# from gerg_plotting.modules.calculations import get_center_of_mass
# import matplotlib
# import numpy as np
# import pyvista as pv
# import pandas as pd


# # # Test Glider Data

# data = data_from_netcdf('C:/Users/alecmkrueger/Documents/GERG/GERG_GitHub/GERG-Glider/Code/Packages/gerg_plotting/docs/examples/example_data/sample_glider_data.nc',interp_glider=True)

# data.detect_bounds(bounds_padding=2)

# def generate_points(data:Data):
#     """A helper to make a 3D NumPy array of points (n_points by 3)"""
#     points = [[lon,lat,depth] for lon,lat,depth in zip(data.lon.values,data.lat.values,data.depth.values)]
    
#     return np.array(points)

# points = generate_points(data)

# glider_data = pv.PolyData(points)


# # Add that data to the mesh with the name "uniform dist"
# glider_data[data.temperature.get_label()] = data.temperature.values


# # Test Bathymetry Data

# df = pd.read_csv('C:/Users/alecmkrueger/Documents/GERG/GERG_GitHub/GERG-Glider/Code/Packages/gerg_plotting/docs/examples/example_data/gom_srtm30_plus.txt',sep='\t')

# # Flip z data
# df['z'] = df['z']*-1

# filtered_df = df[
#     (df['long'] >= data.bounds.lon_min) & 
#     (df['long'] <= data.bounds.lon_max) & 
#     (df['lat'] >= data.bounds.lat_min) & 
#     (df['lat'] <= data.bounds.lat_max)
# ]

# coords = filtered_df.values

# # Make the structured surface manually
# structured = pv.StructuredGrid()
# # Set coordinates
# structured.points = coords
# # Set the dimensions of the structured grid
# structured.dimensions = [len(filtered_df.long.unique()), len(filtered_df.lat.unique()), 1]

# # Apply an Elevation filter
# elevation = structured.elevation()

# # Adjust the colormap
# cmap = cmocean.tools.crop_by_percent(matplotlib.colormaps.get_cmap('Blues'), 10, 'min')
# # Set the under color (land color) for the colormap
# land_color = [231 / 255, 194 / 255, 139 / 255]
# cmap.set_under(land_color)

# elevation['Depth (m)'] = elevation.points[:, 2]

# # Visualize the structured grid
# plotter = pv.Plotter()

# sargs = dict(height=0.5, vertical=True, position_x=0.08, position_y=0.05,below_label='',fmt="%.1f",)
# annotations = {data.depth.values.min(): 'Glider/nMax/nDepth'}
# plotter.add_mesh(elevation, scalars='Depth (m)', cmap=cmap, show_edges=False, lighting=True,
#                  below_color=land_color,clim=(0,filtered_df.z.max()),flip_scalars=False,scalar_bar_args=sargs,annotations=annotations)

# sargs = dict(height=0.5, vertical=True, position_x=0.85, position_y=0.05)
# plotter.add_mesh(glider_data, scalars=data.temperature.get_label(), cmap=data.temperature.cmap, 
#                  show_edges=True, lighting=True,scalar_bar_args=sargs)


# # Access the camera
# plotter.camera.azimuth = -100
# plotter.camera.elevation = 5
# plotter.camera.zoom(1.35)
# plotter.camera.focal_point = get_center_of_mass(lon=data.lon.values,lat=data.lat.values,pressure=data.depth.values)
# plotter.set_scale(1, 1, -0.001)
# # plotter.show(window_size=[1000,1000],interactive=True)
# # scalar_bar = plotter.scalar_bar
# # title_text  = scalar_bar.GetTitleTextProperty()
# # print(type(title_text))
# # title_text.SetJustificationToLeft()
# # import vtkmodules.vtkRenderingCore
# # dir(vtkmodules.vtkRenderingCore.vtkTextProperty)
# # plotter.show()

