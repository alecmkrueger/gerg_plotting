"""
Set vmin and vmax for Plot
===============================

This example shows how to set the vmin and vmax for a variable for a plot.
"""

# %%
# Load the sample data
# ----------------------------------
from gerg_plotting import data_from_netcdf,ScatterPlot

data = data_from_netcdf('example_data/sample_glider_data.nc'
                        ,interp_glider=True,bounds_padding=1.5)

# Show the default unsliced data
plotter_data = ScatterPlot(data)
plotter_data.hovmoller('salinity')
plotter_data.show()

# %%
# Set the vmin and vmax for the salinty variable
# ----------------------------------
data.salinity.vmin = 35.5
data.salinity.vmax = 37
# Show the default unsliced data
plotter_data = ScatterPlot(data)
plotter_data.hovmoller('salinity')
plotter_data.show()