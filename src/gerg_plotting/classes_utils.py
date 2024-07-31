import numpy as np

def lat_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lat_max:
            raise ValueError("'lat_min' must to be smaller than 'lat_max'")
    
def lon_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lon_max:
            raise ValueError("'lon_min' must to be smaller than 'lon_max'")
        
def validate_array_lengths(instance,attribute,value):
    lengths = {attr.name:len(getattr(instance,attr.name)) for attr in instance.__attrs_attrs__ if isinstance(getattr(instance,attr.name),np.ndarray)}
    if len(set(lengths.values()))>1:
        raise ValueError(f'All Dims and Vars must be the same length, got lengths of {lengths}')

        
def get_center_of_mass(lon,lat,pressure) -> tuple:
    centroid = tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])
    return centroid

