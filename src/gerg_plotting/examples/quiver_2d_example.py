from gerg_plotting import Data,MapPlot,data_from_csv,data_from_df,Bathy,ScatterPlot
import matplotlib.pyplot as plt
import pandas as pd
import cmocean

data = data_from_csv('example_data/sample_tabs_data.csv')

data.speed.units = 'cm/s'

scatter = ScatterPlot(data)
scatter.quiver2d(x='time',y='depth',quiver_scale=800)
scatter.ax.invert_yaxis()

plt.show()
