"""
Simple map plot
===================================

Example of a simple map plot.

"""
from gerg_plotting import data_from_netcdf,MapPlot

data = data_from_netcdf('C:/Users/alecmkrueger/Documents/GERG/GERG_GitHub/GERG-Glider/Code/Packages/gerg_plotting/docs/examples/example_data/sample_glider_data.nc',interp_glider=True)

data.detect_bounds(bounds_padding=1.5)

data.time.cmap = 'viridis'

plotter = MapPlot(data)
plotter.scatter('time',show_bathy=True,show_coastlines=False)

plotter.save('example_plots/map_simple.png')
