"""
Data From Netcdf Example with Custom Variables
==============================================

How to use the data_from_netcdf function to load data from a netcdf file.

We also show how to include custom_vars into data with data_from_netcdf

We also plot a hovmoller plot of m_pressure.

"""
from gerg_plotting.tools import data_from_netcdf
from gerg_plotting.plotting_classes import ScatterPlot

# Read in the data from a netcdf file
data = data_from_netcdf("example_data/sample_glider_data.nc",
                        interp_glider=True,custom_vars='m_pressure')
# Set the label for the custom variable to look better
data.custom_variables['m_pressure'].label = 'Mission Pressure'
# Plot the data
scatter = ScatterPlot(data)
scatter.hovmoller('m_pressure')
scatter.save('example_plots/data_from_netcdf_with_custom_vars_example.png')


