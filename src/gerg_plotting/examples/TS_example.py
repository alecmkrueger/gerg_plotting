from gerg_plotting import ScatterPlot,data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Initialize the scatter plot
scatter = ScatterPlot(data)
# Plot just the TS diagram
scatter.TS()
# Plot the TS diagram with a color variable
scatter.TS(color_var='salinity')
