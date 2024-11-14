import matplotlib.pyplot as plt
import matplotlib.axes as maxes
import numpy as np
import pandas as pd
import xarray as xr
import gsw
import datetime
from typing import Iterable
from matplotlib.colors import ListedColormap

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

def to_numpy_array(values:Iterable):
    # Convert iterable types (list, tuple, pandas.Series, etc.) to NumPy array
    if not isinstance(values, np.ndarray):
        array = pd.Series(values).to_numpy()
        return array
    elif isinstance(values, np.ndarray):
        return values
    elif values is None:
        return None
    else:
        raise ValueError(f"Cannot convert {type(value)} to a NumPy array")

def is_flat_numpy_array(instance, attribute, value):
    # Validate that the value is now a NumPy array
    if not isinstance(value, np.ndarray):
        raise ValueError(f"{attribute.name} must be a NumPy array or a list convertible to a NumPy array")
    
    # Ensure the array is flat (1-dimensional)
    if value.ndim != 1:
        raise ValueError(f"{attribute.name} must be a flat array")
    
def get_center_of_mass(lon,lat,pressure) -> tuple:
    centroid = tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])
    return centroid

def filter_var(var:pd.Series,min_value,max_value):
    var = var.where(var>min_value)
    var = var.where(var<max_value)
    return var

def calculate_range(var:np.ndarray):
    return [np.nanmin(var),np.nanmax(var)]

def calculate_pad(var:np.ndarray,pad=0.0):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference*pad
    start = start-pad
    stop = stop+pad
    start = float(start)
    stop = float(stop)
    return start,stop

def colorbar(fig,divider,mappable,label:str,nrows:int=1,total_cbars:int=2):
    last_axes = plt.gca()
    base_pad = 0.1
    num_colorbars = (len(fig.axes)-nrows)%total_cbars
    pad = base_pad + num_colorbars * 0.6
    cax = divider.append_axes("right", size="4%", pad=pad,axes_class=maxes.Axes)
    cbar = fig.colorbar(mappable, cax=cax,label=label)
    plt.sca(last_axes)
    return cbar

def get_sigma_theta(salinity:np.ndarray,temperature:np.ndarray,cnt:bool=False):
    # Subsample the data
    num_points = len(temperature)
    if num_points>50_000 and num_points<300_000:
        salinity = salinity[::100]
        temperature = temperature[::100]    
    elif num_points>300_000 and num_points<1_000_000:
        salinity = salinity[::250]
        temperature = temperature[::250]
    elif num_points>=1_000_000:
        salinity = salinity[::1000]
        temperature = temperature[::1000]        

    # Remove nan values
    salinity = salinity[~np.isnan(salinity.astype('float64'))]
    temperature = temperature[~np.isnan(temperature.astype('float64'))]

    mint=np.min(temperature)
    maxt=np.max(temperature)

    mins=np.min(salinity)
    maxs=np.max(salinity)

    num_points = len(temperature)

    tempL=np.linspace(mint-1,maxt+1,num_points)

    salL=np.linspace(mins-1,maxs+1,num_points)

    Tg, Sg = np.meshgrid(tempL,salL)
    sigma_theta = gsw.sigma0(Sg, Tg)

    if cnt:
        num_points = len(temperature)
        cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),num_points)
        return Sg, Tg, sigma_theta, cnt
    else:
        return Sg, Tg, sigma_theta


def get_density(salinity,temperature):
    return gsw.sigma0(salinity, temperature)

def rotate_vector(u,v,theta_rad):
    u_rotated = u * np.cos(theta_rad) - v * np.sin(theta_rad)
    v_rotated = u * np.sin(theta_rad) + v * np.cos(theta_rad)
    return u_rotated,v_rotated

def filter_nan(values):
    return values[~np.isnan(values)]

def get_turner_cmap():
    # Define the number of colors
    n_colors = 256

    # Create an array of RGBA colors from an existing colormap, here 'viridis'
    viridis = plt.cm.get_cmap('viridis', n_colors)
    newcolors = viridis(np.linspace(0, 1, n_colors))

    # Define colors for each range
    red = np.array([1, 0, 0, 1])       # RGBA for red
    yellow = np.array([1, 1, 0, 1])    # RGBA for yellow
    green = np.array([0, 1, 0, 1])     # RGBA for green
    blue = np.array([0, 0, 1, 1])      # RGBA for blue

    # Assign colors to specific ranges
    newcolors[:int(256 * 0.125)] = red    # Values below -90
    newcolors[int(256 * 0.125):int(256 * 0.375)] = yellow  # Values between -90 and -45
    newcolors[int(256 * 0.375):int(256 * 0.625)] = green   # Values between -45 and 45
    newcolors[int(256 * 0.625):int(256 * 0.875)] = blue    # Values between 45 and 90
    newcolors[int(256 * 0.875):] = red    # Values above 90

    # Create the ListedColormap
    newcmp = ListedColormap(newcolors)

    return newcmp


def print_time(value: int = None, intervals: list = [10,50,100,500,1000]):
    """
    Prints the current time if the value matches any of the intervals specified.

    Args:
    - value (int): The value value.
    - intervals (list): A list of integers representing intervals.

    Returns:
    - None
    """

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if value is None:
        print(current_time)
        return

    # Check if intervals is at least 2 values long
    if not len(intervals) >= 2:
        raise ValueError(f'Not enough intervals, need at least 2 values, you passed {len(intervals)}')


    if value <= intervals[0]:
        print(f'{value = }, {current_time}')
        return
    elif value <= intervals[-2]:
        for idx,interval in enumerate(intervals[0:-1]):
            if value >= interval:
                if value < intervals[idx+1]:
                    if value % interval==0:
                        print(f'{value = }, {current_time}')
                        return
                    break
    elif value >= intervals[-1]:
        if value % intervals[-1]==0:
            print(f'{value = }, {current_time}')
            return


def calculate_range(var:np.ndarray):
    return [np.nanmin(var),np.nanmax(var)]

def calculate_pad(var:np.ndarray,pad=0.0):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference*pad
    start = start-pad
    stop = stop+pad
    start = float(start)
    stop = float(stop)
    return start,stop

def colorbar(fig,divider,mappable,label:str,nrows:int=1,total_cbars:int=2):
    last_axes = plt.gca()
    base_pad = 0.1
    num_colorbars = (len(fig.axes)-nrows)%total_cbars
    pad = base_pad + num_colorbars * 0.6
    cax = divider.append_axes("right", size="4%", pad=pad,axes_class=maxes.Axes)
    cbar = fig.colorbar(mappable, cax=cax,label=label)
    plt.sca(last_axes)
    return cbar

def get_sigma_theta(salinity:np.ndarray,temperature:np.ndarray,cnt:bool=False):
    # Subsample the data
    num_points = len(temperature)
    if num_points>50_000 and num_points<300_000:
        salinity = salinity[::100]
        temperature = temperature[::100]    
    elif num_points>300_000 and num_points<1_000_000:
        salinity = salinity[::250]
        temperature = temperature[::250]
    elif num_points>=1_000_000:
        salinity = salinity[::1000]
        temperature = temperature[::1000]        

    # Remove nan values
    salinity = salinity[~np.isnan(salinity.astype('float64'))]
    temperature = temperature[~np.isnan(temperature.astype('float64'))]

    mint=np.min(temperature)
    maxt=np.max(temperature)

    mins=np.min(salinity)
    maxs=np.max(salinity)

    num_points = len(temperature)

    tempL=np.linspace(mint-1,maxt+1,num_points)

    salL=np.linspace(mins-1,maxs+1,num_points)

    Tg, Sg = np.meshgrid(tempL,salL)
    sigma_theta = gsw.sigma0(Sg, Tg)

    if cnt:
        num_points = len(temperature)
        cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),num_points)
        return Sg, Tg, sigma_theta, cnt
    else:
        return Sg, Tg, sigma_theta


def get_density(salinity,temperature):
    return gsw.sigma0(salinity, temperature)

def rotate_vector(u,v,theta_rad):
    u_rotated = u * np.cos(theta_rad) - v * np.sin(theta_rad)
    v_rotated = u * np.sin(theta_rad) + v * np.cos(theta_rad)
    return u_rotated,v_rotated

def filter_nan(values):
    return values[~np.isnan(values)]

def get_turner_cmap():
    # Define the number of colors
    n_colors = 256

    # Create an array of RGBA colors from an existing colormap, here 'viridis'
    viridis = plt.cm.get_cmap('viridis', n_colors)
    newcolors = viridis(np.linspace(0, 1, n_colors))

    # Define colors for each range
    red = np.array([1, 0, 0, 1])       # RGBA for red
    yellow = np.array([1, 1, 0, 1])    # RGBA for yellow
    green = np.array([0, 1, 0, 1])     # RGBA for green
    blue = np.array([0, 0, 1, 1])      # RGBA for blue

    # Assign colors to specific ranges
    newcolors[:int(256 * 0.125)] = red    # Values below -90
    newcolors[int(256 * 0.125):int(256 * 0.375)] = yellow  # Values between -90 and -45
    newcolors[int(256 * 0.375):int(256 * 0.625)] = green   # Values between -45 and 45
    newcolors[int(256 * 0.625):int(256 * 0.875)] = blue    # Values between 45 and 90
    newcolors[int(256 * 0.875):] = red    # Values above 90

    # Create the ListedColormap
    newcmp = ListedColormap(newcolors)

    return newcmp


def print_time(value: int = None, intervals: list = [10,50,100,500,1000]):
    """
    Prints the current time if the value matches any of the intervals specified.

    Args:
    - value (int): The value value.
    - intervals (list): A list of integers representing intervals.

    Returns:
    - None
    """

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if value is None:
        print(current_time)
        return

    # Check if intervals is at least 2 values long
    if not len(intervals) >= 2:
        raise ValueError(f'Not enough intervals, need at least 2 values, you passed {len(intervals)}')


    if value <= intervals[0]:
        print(f'{value = }, {current_time}')
        return
    elif value <= intervals[-2]:
        for idx,interval in enumerate(intervals[0:-1]):
            if value >= interval:
                if value < intervals[idx+1]:
                    if value % interval==0:
                        print(f'{value = }, {current_time}')
                        return
                    break
    elif value >= intervals[-1]:
        if value % intervals[-1]==0:
            print(f'{value = }, {current_time}')
            return

def interp_glider_lat_lon(ds) -> xr.Dataset:
    # Convert time and m_time to float64 for interpolation
    new_time_values = ds['time'].values.astype('datetime64[s]').astype('float64')
    new_mtime_values = ds['m_time'].values.astype('datetime64[s]').astype('float64')

    # Create masks of non-NaN values for both latitude and longitude
    valid_latitude = ~np.isnan(ds['latitude'])
    valid_longitude = ~np.isnan(ds['longitude'])

    # Interpolate latitude based on valid latitude and m_time values
    ds['latitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_latitude], ds['latitude'].values[valid_latitude]),
        [('time', ds['time'].values)]
    )

    # Interpolate longitude based on valid longitude and m_time values
    ds['longitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_longitude], ds['longitude'].values[valid_longitude]),
        [('time', ds['time'].values)]
    )

    ds = ds.drop_vars('m_time')

    return ds

def map_variables(keys, values, synonyms=None, blocklist=None):
    """
    Maps each key from the keys list to the most likely corresponding value from the values list,
    using optional synonyms and blocklist terms for flexible and precise matching.
    
    Parameters:
    - keys (list): List of keys to be used in the dictionary.
    - values (list): List of possible values to map to keys.
    - synonyms (dict, optional): Dictionary where each key has a list of synonyms to assist in matching.
    - blocklist (dict, optional): Dictionary where each key has a list of words to avoid for that key.
    
    Returns:
    - dict: Dictionary mapping each key to a corresponding value or None if no match is found.
    """
    # Initialize the dictionary with None for each key
    mapped_dict = {key: None for key in keys}
    
    # Iterate through each key
    for key in keys:
        # Gather possible matches, starting with the key itself
        possible_matches = [key]
        
        # Add synonyms if provided
        if synonyms and key in synonyms:
            possible_matches.extend(synonyms[key])
        
        # Get blocked words for the key if provided
        blocked_words = blocklist.get(key, []) if blocklist else []
        
        # Search through values for matches
        for value in values:
            # Check if this is a single-letter key (like 'u' or 'v')
            if len(key) == 1:
                # Ensure the key appears only at the start or end of the value string
                if (value.lower().startswith(key.lower()) or value.lower().endswith(key.lower())):
                    mapped_dict[key] = value
                    break
            else:
                # Check for matching while excluding blocked words
                if (any(match.lower() in value.lower() for match in possible_matches) and
                    all(block.lower() not in value.lower() for block in blocked_words)):
                    mapped_dict[key] = value
                    break
    
    return mapped_dict


def get_var_mapping(df) -> dict:
    keys = ['lat', 'lon', 'depth', 'time', 'temperature', 'salinity', 'density', 'u', 'v','w', 'speed']
    values = df.columns.tolist()
    synonyms = {
        'depth': ['pressure', 'pres'],
        'temperature': ['temp', 'temperature_measure'],
        'salinity': ['salt', 'salinity_level'],
        'density': ['density_metric', 'rho'],
        'u': ['eastward_velocity', 'u_component'],
        'v': ['northward_velocity', 'v_component'],
        'w': ['downward_velocity','upward_velocity','w_component'],
        's': ['combined_velocity','velocity','speed']
    }
    blocklist = {
        's': ['sound']
    }

    mapped_variables = map_variables(keys, values, synonyms, blocklist)

    return mapped_variables
