from gerg_plotting.plotting_classes.scatter_plot_3d import ScatterPlot3D
from gerg_plotting import data_from_netcdf,Data,cmocean


data = data_from_netcdf('C:/Users/alecmkrueger/Documents/GERG/GERG_GitHub/GERG-Glider/Code/Packages/gerg_plotting/docs/examples/example_data/sample_glider_data.nc',interp_glider=True)

data.detect_bounds(bounds_padding=2)

data.bounds.vertical_scalar = -0.001

plotter = ScatterPlot3D(data,figsize=(1280,720))

plotter.map('temperature')

plotter.show()
