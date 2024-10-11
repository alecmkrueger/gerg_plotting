'''
Thin wrapper around matplotlib for standarized plotting at GERG
'''

from .plotting_classes.Histogram import Histogram
from .plotting_classes.Animator import Animator
from .data_classes.NonSpatialInstruments import Bounds
from .data_classes.SpatialInstruments import Bathy,Data
from .plotting_classes.SurfacePlot import SurfacePlot
from .plotting_classes.VarPlot import VarPlot