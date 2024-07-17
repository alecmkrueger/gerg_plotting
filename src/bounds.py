from attrs import define,field,asdict,validators
from warnings import warn
from pprint import pformat

from utils.class_utils import lat_min_smaller_than_max,lon_min_smaller_than_max

@define
class Bounds:
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)

    # If the longitude is -180 to 180 then the state is relative
    # If the longitude is 0 to 360 then the state is absolute
    longitude_state:str|None = field(default=None)

    def __attrs_post_init__(self):
        if self.longitude_state is None:
            self.determine_longitude_state()

    def determine_longitude_state(self):
        if self.lon_min > 0 or self.lon_max>0:
            warn('The longitude state might be incorrect, please verify or pass the state')
        elif self.lon_min<0 or self.lon_max<0:
            self.longitude_state = 'relative'
        elif (0 <= self.lon_min <= 360) or (0 <= self.lon_max <= 360):
            self.longitude_state = 'absolute'

    def relative_longitude(self):
        # Convert the longitude to relative i.e. from 0-360 to -180-180
        if self.longitude_state == 'absolute':
            if self.lon_min is not None:
                self.lon_min = self.lon_min-180
            if self.lon_max is not None:
                self.lon_max = self.lon_max-180
            self.longitude_state = 'relative'
        else:
            raise ValueError('longitude must be absolute before converting to relative')

    def absoloute_longitude(self):
        # Convert the longitude to absolute i.e. from -180-180 to 0-360 
        if self.longitude_state == 'relative': 
            if self.lon_min is not None:
                self.lon_min = self.lon_min+180
            if self.lon_max is not None:
                self.lon_max = self.lon_max+180
            self.longitude_state = 'absolute'
        else:
            raise ValueError('longitude must be relative before converting to relative')

    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)
    def __getitem__(self, key:str):
        return asdict(self)[key]