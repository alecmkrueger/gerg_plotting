from gerg_plotting.plotting_classes.ScatterPlot import ScatterPlot
from gerg_plotting.tools import data_from_csv

data = data_from_csv('example_data/glider_data.csv')

plotter = ScatterPlot(data=data)

# plotter.
