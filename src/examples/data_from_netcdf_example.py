from gerg_plotting.tools.tools import data_from_netcdf
from gerg_plotting.plotting_classes import Histogram, ScatterPlot

import xarray as xr

def data_from_netcdf_example():
    """
    Data From Netcdf Example
    -----------
    Source Code
    ~~~~~~~~~~
    .. literalinclude:: ../../../src\examples\data_from_netcdf_example.py
       :language: python

    Output
    ~~~~~~
    .. image:: ../../../src\examples\data_from_netcdf_example.png
       :width: 600
    
    """
    data = data_from_netcdf("example_data/sample_glider_data.nc",
                            interp_glider=True)
        
    hist = Histogram(data)
    hist.plot('lat')

    scatter = ScatterPlot(data)
    scatter.hovmoller('temperature')
    scatter.hovmoller('chlor')

if __name__ == "__main__":
    data_from_netcdf_example()