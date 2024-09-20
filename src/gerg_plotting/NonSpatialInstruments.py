from attrs import define,field,asdict,validators
from matplotlib.colors import Colormap
import cmocean
from pprint import pformat
import numpy as np

from gerg_plotting.utils import lat_min_smaller_than_max,lon_min_smaller_than_max
from gerg_plotting.NonSpatialInstrument import NonSpatialInstrument


@define
class Variable(NonSpatialInstrument):
    data:np.ndarray
    name:str
    cmap:Colormap
    units:str
    vmin:float
    vmax:float

    
# @define
# class CMaps(NonSpatialInstrument):
#     temperature:Colormap = field(default=cmocean.cm.thermal)
#     salinity:Colormap = field(default=cmocean.cm.haline)
#     density:Colormap = field(default=cmocean.cm.dense)
#     depth:Colormap = field(default=cmocean.tools.crop_by_percent(cmocean.cm.deep,7,'both'))
#     u_current:Colormap = field(default=cmocean.cm.delta)
#     v_current:Colormap = field(default=cmocean.cm.delta)
#     time:Colormap = field(default=cmocean.cm.thermal)

# @define
# class Units(NonSpatialInstrument):
#     temperature:str = field(default='°C')
#     salinity:str = field(default='')
#     density:str = field(default="kg/m\u00B3")
#     depth:str = field(default='m')
#     u_current:str = field(default='cm/s')
#     v_current:str = field(default='cm/s')
#     s_current:str = field(default='cm/s')


class Lab(NonSpatialInstrument):
    def __init__(self,vars):
        for key,value in vars.items():
            setattr(self,key,value)

@define
class Bounds(NonSpatialInstrument):
    '''
    depth_bottom: positive depth example: 1000 meters
    depth_top:positive depth example: 0 meters
    '''
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)