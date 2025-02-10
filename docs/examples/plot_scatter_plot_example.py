"""
Scatter Plot Example
===================================

Example scatter plot.

"""
from gerg_plotting import ScatterPlot, data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Let's subsample the dataset
data = data[::50]

scatter = ScatterPlot(data)
scatter.scatter('time','temperature')
scatter.save('example_plots/scatter_plot_example.png',bbox_inches='tight')
