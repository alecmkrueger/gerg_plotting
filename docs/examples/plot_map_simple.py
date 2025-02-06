"""
Simple map plot
===================================

Example of a simple map plot.

"""
from gerg_plotting import data_from_netcdf,MapPlot

data = data_from_netcdf('example_data/sample_glider_data.nc',interp_glider=True,bounds_padding=1.5)

plotter = MapPlot(data)
plotter.scatter('time',show_bathy=True,show_coastlines=False)

plotter.save('example_plots/map_simple.png')
