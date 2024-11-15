from attrs import define,field,validators,asdict
from pprint import pformat

from gerg_plotting.modules.validations import lat_min_smaller_than_max,lon_min_smaller_than_max

@define
class Bounds():
    '''
    depth_bottom: positive depth example: 1000
    depth_top:positive depth example for surface: 0
    '''
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int|None = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)


    def _has_var(self, key):
        return key in asdict(self).keys()
    def __getitem__(self, key):
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Attribute '{key}' not found")
    def __setitem__(self, key, value):
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)