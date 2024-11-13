from gerg_plotting import Bounds,ScatterPlot,data_from_csv
from gerg_plotting.plotting_classes.utils import generate_random_point
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean

# Define bounds
bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
# Let's read in the example data
data = data_from_csv('example_data/sample_glider_data.csv')

scatter = ScatterPlot(data).scatter('time','depth')
