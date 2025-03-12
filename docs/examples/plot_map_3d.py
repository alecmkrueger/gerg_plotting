"""
Plot a 3D Map
=====================================================

How to use gerg_plotting to plot a 3D map.

"""

from gerg_plotting import data_from_netcdf,ScatterPlot3D

# Read in the data, interpolating the glider data, and setting the bounds padding to 1.5 degrees
data = data_from_netcdf('example_data/sample_glider_data.nc',interp_glider=True,bounds_padding=1.5)
# Set the vertical scalar the data by a factor of 1000 and flip the depth data so down is negative
data.bounds.vertical_scalar = -0.001
# Set the depth bounds to None so we can see all of the bathymetry
data.bounds.depth_bottom = None
data.bounds.depth_top = None
plotter = ScatterPlot3D(data)
plotter.map('temperature',show_plot=True)
plotter.save('example_plots/map_3d.png')
plotter.export_html('example_plots/map_3d.html')

