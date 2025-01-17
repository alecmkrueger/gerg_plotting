"""
Data From Netcdf Example
===================================

How to use the data_from_netcdf function to load data from a netcdf file.
We also plot a hovmoller plot of chlorophyll 

.. image:: ../examples/example_plots/data_from_netcdf_example.png
    :alt: Pre-generated image for this example

"""
from gerg_plotting.tools import data_from_netcdf
from gerg_plotting.plotting_classes import ScatterPlot


data = data_from_netcdf("example_data/sample_glider_data.nc",
                        interp_glider=True)
    
scatter = ScatterPlot(data)
scatter.hovmoller('chlor')
scatter.save('example_plots/data_from_netcdf_example.png')


