"""
Hovmoller Example
===================================

Example of a Hovmoller plot.

"""
from gerg_plotting import ScatterPlot, data_from_csv

# Let's read in some example data
data = data_from_csv('example_data/sample_glider_data.csv')

scatter = ScatterPlot(data)

scatter.hovmoller('temperature')

scatter.save('example_plots/hovmoller_example.png',dpi=300)
