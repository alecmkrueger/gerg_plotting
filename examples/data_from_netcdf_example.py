"""
Data From Netcdf Example
===================================

How to use the data_from_netcdf function to load data from a netcdf file.
We also plot a histogram of salinity and hovmoller plots for temperature and chlorophyll 

"""
from gerg_plotting.tools import data_from_netcdf
from gerg_plotting.plotting_classes import Histogram, ScatterPlot


data = data_from_netcdf("example_data/sample_glider_data.nc",
                        interp_glider=True)
    
Histogram(data).plot('salinity')

scatter = ScatterPlot(data)
scatter.hovmoller('temperature')
scatter.hovmoller('chlor')
