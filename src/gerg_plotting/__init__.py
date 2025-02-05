'''
A module for standardized plotting at GERG
'''

from .plotting_classes.animator import Animator
from .plotting_classes.coverage_plot import CoveragePlot
from .plotting_classes.histogram import Histogram
from .plotting_classes.map_plot import MapPlot
from .plotting_classes.scatter_plot import ScatterPlot
from .plotting_classes.scatter_plot_3d import ScatterPlot3D
from .data_classes.bathy import Bathy
from .data_classes.variable import Variable
from .data_classes.bounds import Bounds
from .data_classes.data import Data
from .tools.tools import data_from_df,data_from_csv,data_from_netcdf,data_from_ds,interp_glider_lat_lon
from .download_example_data import download_example_data
import cmocean
