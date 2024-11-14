from gerg_plotting import ScatterPlot3D,Bathy,data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

data_bounds = data.detect_bounds(bounds_padding=0.75)

bathy = Bathy(bounds=data_bounds,resolution_level=5)

# Init the 3-d scatter plot
three_d = ScatterPlot3D(data,bathy=bathy)
three_d.map(var='temperature',vertical_scalar=-1000)
