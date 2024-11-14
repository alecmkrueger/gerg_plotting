import numpy as np
import pandas as pd
import xarray as xr

from gerg_plotting.modules.utils import get_var_mapping
from gerg_plotting.data_classes.SpatialInstruments import Data

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
        mapped_variables = get_var_mapping(df)

    mapped_variables = {key:df[value] for key,value in mapped_variables.items() if value is not None}

    data = Data(**mapped_variables)

    return data

def data_from_csv(filename:str,mapped_variables:dict|None=None):

    df = pd.read_csv(filename)

    data = data_from_df(df,mapped_variables=mapped_variables)

    return data
