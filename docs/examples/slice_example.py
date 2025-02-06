from gerg_plotting import data_from_netcdf
import numpy as np

data = data_from_netcdf('example_data/sample_glider_data.nc',interp_glider=True,bounds_padding=1.5)

# Get the dates
dates = data.time.values
# Define the start and end dates
start_date = np.datetime64('2024-08-18')
end_date = np.datetime64('2024-12-18')
# Slice the data based on the dates
data_sliced = data[(dates >= start_date) & (dates <= end_date)]



