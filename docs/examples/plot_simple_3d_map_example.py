"""
Simple 3D Map Example
===================================

Example description

.. image:: ../examples/example_plots/simple_3d_map_example.png
    :alt: Pre-generated image for this example

"""
from gerg_plotting.plotting_classes import ScatterPlot3D
from gerg_plotting.tools import data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Let's plot the 3d data
scatter = ScatterPlot3D(data)
scatter.map(var='temperature',vertical_scalar=-1000,bounds_padding=0.3,show=False)
scatter.save('example_plots/simple_3d_map_example.png')
# scatter.show()
