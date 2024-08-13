'''
Thin wrapper on matplotlib for standarized plotting at GERG
'''

from .Histogram import Histogram
from .Animator import Animator
from .NonSpatialInstruments import Lab,Bounds,CMaps,Units
from .SpatialInstruments import Bathy,Glider,Buoy,CTD,WaveGlider,Radar
from .SurfacePlot import SurfacePlot
from .VarPlot import VarPlot