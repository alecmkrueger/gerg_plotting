import numpy as np
from attrs import define, field
from src.utils.class_utils import check_lat,check_lon

@define
class Glider:
    # Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray

@define
class Buoy:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray
    u_current:np.ndarray
    v_current:np.ndarray

@define
class CTD:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray

@define
class WaveGlider:
    #Dims
    lat:np.ndarray
    lon:np.ndarray
    depth:np.ndarray
    time:np.ndarray
    # Vars
    temperature:np.ndarray
    salinity:np.ndarray 

