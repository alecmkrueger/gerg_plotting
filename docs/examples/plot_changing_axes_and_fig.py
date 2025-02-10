"""
Changing axes and figure visualization
==================================================

How to modify a plot using fig and ax.

"""
from gerg_plotting import ScatterPlot, data_from_csv

# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

# Initialize the scatter plot
scatter = ScatterPlot(data)
# Plot the TS diagram with a color variable
scatter.TS(color_var='depth',contours=False)

# ScatterPlot.ax is a matplotlib.axes.Axes object
# zoom out a bit
scatter.ax.set_ylim((3,33.5))
scatter.ax.set_xlim(31.5,37.5)
# Make the colors pop
scatter.ax.set_facecolor('gray')

# ScatterPlot.fig is a matplotlib.figure.Figure object
# Let's change the title from "T-S Diagram" to something more descriptive
scatter.ax.set_title('T-S Diagram with Depth',fontdict={'fontsize':14,'fontweight':'bold'})

scatter.save('example_plots/modifying_plot.png',bbox_inches='tight')

scatter.show()
