from gerg_plotting import Bounds,ScatterPlot,data_from_csv


def simple_scatter_plot():

    # Define bounds
    bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
    # Let's read in the example data
    data = data_from_csv('example_data/sample_glider_data.csv')

    scatter = ScatterPlot(data)
    scatter.scatter('time','temperature')
    scatter.save('example_plots/simple_scatter_plot.png')

if __name__ == "__main__":
    simple_scatter_plot()