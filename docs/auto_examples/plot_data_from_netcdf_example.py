"""
Data From Netcdf Example
===================================

How to use the data_from_netcdf function to load data from a netcdf file.
We also plot a hovmoller plot of chlorophyll 

"""
from gerg_plotting import data_from_netcdf, ScatterPlot


data = data_from_netcdf("example_data/sample_glider_data.nc",
                        interp_glider=True)

scatter = ScatterPlot(data)
scatter.hovmoller('chlor')
scatter.save('example_plots/data_from_netcdf_example.png')


