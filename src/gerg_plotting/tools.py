import numpy as np
import pandas as pd
import xarray as xr

from gerg_plotting.data_classes.Data import Data


def _map_variables(keys, values, synonyms=None, blocklist=None):
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


def _get_var_mapping(df) -> dict:
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

    mapped_variables = _map_variables(keys, values, synonyms, blocklist)

    return mapped_variables


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


def data_from_df(df:pd.DataFrame,mapped_variables:dict|None=None):

    # If the user does not pass mapped_variables
    if mapped_variables is None:
        mapped_variables = _get_var_mapping(df)

    mapped_variables = {key:df[value] for key,value in mapped_variables.items() if value is not None}

    data = Data(**mapped_variables)

    return data


def data_from_csv(filename:str,mapped_variables:dict|None=None):

    df = pd.read_csv(filename)

    data = data_from_df(df,mapped_variables=mapped_variables)

    return data