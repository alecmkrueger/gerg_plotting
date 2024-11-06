from gerg_plotting import Data,MapPlot,data_from_csv,data_from_df,Bathy
import matplotlib.pyplot as plt
import pandas as pd
import cmocean

data = data_from_csv('example_data/sample_radar_data.csv')

MapPlot(data).quiver(quiver_density=200)

plt.show()
