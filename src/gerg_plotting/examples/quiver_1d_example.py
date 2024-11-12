from gerg_plotting import ScatterPlot,data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_radar_data.csv')

ScatterPlot(data).quiver1d(x='time',quiver_scale=1)
