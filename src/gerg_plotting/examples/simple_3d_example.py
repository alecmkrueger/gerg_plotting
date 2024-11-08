from gerg_plotting import ScatterPlot3D,data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Let's plot the 3d data
ScatterPlot3D(data).map(var='temperature',vertical_scalar=-1000,bounds_padding=0.3)
