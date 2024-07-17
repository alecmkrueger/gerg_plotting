import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

def interp_data(ds:xr.Dataset) -> pd.DataFrame:
    new_time_values = ds['time'].values.astype('datetime64[s]').astype('float64')
    new_mtime_values = ds['m_time'].values.astype('datetime64[s]').astype('float64')

    # Create a mask of non-NaN values in the 'longitude' variable
    valid_longitude = ~np.isnan(ds['longitude'])
    # Now ds_filtered contains the data where NaN values have been dropped based on the longitude variable

    ds['latitude'] = xr.DataArray(np.interp(new_time_values, new_mtime_values[valid_longitude], ds['latitude'].values[valid_longitude]),[('time',ds.time.values)])
    ds['longitude'] = xr.DataArray(np.interp(new_time_values, new_mtime_values[valid_longitude], ds['longitude'].values[valid_longitude]),[('time',ds.time.values)])

    df = ds[['latitude','longitude','pressure','salinity','temperature']].to_dataframe().reset_index()
    df['time'] = df['time'].astype('datetime64[s]')
    # df = df.set_index(['time'])
    df = df.dropna()

    return df


def filter_var(var:pd.Series,min_value,max_value):
    var = var.where(var>min_value)
    var = var.where(var<max_value)
    return var


