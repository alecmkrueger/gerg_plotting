'''
A module for standardized plotting at GERG
'''

from .plotting_classes import Animator,CoveragePlot,Histogram,MapPlot,ScatterPlot,ScatterPlot3D
from .data_classes import Bathy,Variable,Bounds,Data
from .tools import data_from_df,data_from_csv,data_from_netcdf,data_from_ds,interp_glider_lat_lon
import cmocean
