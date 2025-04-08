"""
Plot a 3D Map
=====================================================

How to use gerg_plotting to plot a 3D map.

"""
from pathlib import Path
from gerg_plotting import data_from_netcdf, ScatterPlot3D

# Read in the data, interpolating the glider data, and setting the bounds padding to 1.5 degrees
data_path = Path(__file__).parent.joinpath('example_data/sample_glider_data.nc')
data = data_from_netcdf(data_path,interp_glider=True,bounds_padding=1.5)
# Set the vertical scalar the data by a factor of 1000 and flip the depth data so down is negative
data.bounds.vertical_scalar = -0.001
# Set the depth bounds to None so we can see all of the bathymetry
data.bounds.depth_bottom = None
data.bounds.depth_top = None
# Init plotter
plotter = ScatterPlot3D(data,figsize=(640,480),off_screen=False)
# Plot map
plotter.map('temperature',show_bathy_cbar=False)
# plotter.set_camera(azimuth=-120,elevation=10)
plotter.plotter.focal_point = (0,0,0)
print(plotter.plotter.camera.focal_point)
plotter.show()
print(plotter.plotter.camera.focal_point)

# Save plot as png
# plotter.save(Path(__file__).parent.joinpath('example_plots/map_3d.png'))
# # Save plot as interactive html
# plotter.export_html('example_plots/map_3d.html')

