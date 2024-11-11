from gerg_plotting import data_from_csv,ScatterPlot

# Let's read in some example data
data = data_from_csv('example_data/sample_glider_data.csv')

scatter = ScatterPlot(data)

scatter.hovmoller('temperature')

scatter.fig.savefig('example_plots/temperature_hovmoller.png',dpi=300)
