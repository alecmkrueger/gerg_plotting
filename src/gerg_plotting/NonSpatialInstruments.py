from attrs import define,field,validators
from matplotlib.colors import Colormap
from typing import Iterable

from gerg_plotting.utils import lat_min_smaller_than_max,lon_min_smaller_than_max,is_flat_numpy_array,to_numpy_array
from gerg_plotting.NonSpatialInstrument import NonSpatialInstrument

@define
class Variable(NonSpatialInstrument):
    data:Iterable = field(converter=to_numpy_array,validator=is_flat_numpy_array)
    name:str
    cmap:Colormap
    units:str
    vmin:float
    vmax:float

@define
class Bounds(NonSpatialInstrument):
    '''
    depth_bottom: positive depth example: 1000 meters
    depth_top:positive depth example: 0 meters
    '''
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int|None = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)