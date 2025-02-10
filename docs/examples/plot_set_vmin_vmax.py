"""
Set vmin and vmax for Plot
===============================

This example shows how to set the vmin and vmax for a variable for a plot.
"""

# %%
# Load the sample data
# -----------------------------------------------------------------------
from gerg_plotting import data_from_netcdf,ScatterPlot

data = data_from_netcdf('example_data/sample_glider_data.nc'
                        ,interp_glider=True,bounds_padding=1.5)

# Show the default unsliced data
plotter_data = ScatterPlot(data)
plotter_data.hovmoller('salinity')
plotter_data.show()
plotter_data.save('example_plots/set_vmin_vmax_default.png',bbox_inches='tight')
# %%
# Set the vmin and vmax for the salinty variable
# -----------------------------------------------------------------------
data.salinity.vmin = 34.5
data.salinity.vmax = 37.1
# Show the default unsliced data
plotter_data = ScatterPlot(data)
plotter_data.hovmoller('salinity')
plotter_data.show()
plotter_data.save('example_plots/set_vmin_vmax.png',bbox_inches='tight')
