"""
TS Example
===================================

Example description

.. image:: ../examples/example_plots/TS_example.png
    :alt: Pre-generated image for this example

"""
from gerg_plotting.plotting_classes import ScatterPlot
from gerg_plotting.tools import data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Initialize the scatter plot
scatter = ScatterPlot(data)
# Plot just the TS diagram
scatter.TS()
# Plot the TS diagram with a color variable
scatter.TS(color_var='salinity')

scatter.save('example_plots/TS_example.png')
