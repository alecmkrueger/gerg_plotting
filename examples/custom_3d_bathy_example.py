"""
Custom 3D Bathy Example
===================================

Example description

"""
from gerg_plotting.plotting_classes import ScatterPlot3D
from gerg_plotting.data_classes import Bathy
from gerg_plotting.tools import data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

data_bounds = data.detect_bounds(bounds_padding=0.75)

bathy = Bathy(bounds=data_bounds,resolution_level=5)

# Init the 3-d scatter plot
three_d = ScatterPlot3D(data,bathy=bathy)
three_d.map(var='temperature',vertical_scalar=-1000,show=False)
three_d.save('example_plots/custom_3d_bathy_example.png')
# if you want to show the figure after saving:
# three_d.show()
