from gerg_plotting.plotting_classes.scatter_plot_3d import ScatterPlot3D
from gerg_plotting.modules.calculations import get_center_of_mass

from gerg_plotting.tools import data_from_netcdf

glider_data_path = 'C:/Users/alecmkrueger/Documents/GERG/GERG_GitHub/GERG-Glider/Code/Packages/gerg_plotting/docs/examples/example_data/sample_glider_data.nc'
data = data_from_netcdf(glider_data_path,interp_glider=True)
data.detect_bounds(bounds_padding=2)
data.bounds.vertical_scalar = -0.001

plotter = ScatterPlot3D(data)

# plotter.scatter(x='lon',y='lat',z='depth')
plotter.map('salinity')


plotter.plotter.camera.azimuth = -100
plotter.plotter.camera.elevation = 5
plotter.plotter.camera.zoom(1.35)

plotter.show(window_size=(1920,1080))
