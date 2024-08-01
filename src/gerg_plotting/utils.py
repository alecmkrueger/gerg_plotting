import numpy as np
import pandas as pd
import xarray as xr
import gsw

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

def calculate_range(var:np.ndarray):
    return [np.nanmin(var),np.nanmax(var)]

def calculate_pad(var,pad=0.15):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference*pad
    start = start-pad
    stop = stop+pad
    return start,stop

def get_sigma_theta(salinity,temperature,cnt=False):
    # Subsample the data 
    salinity = salinity[::100]
    temperature = temperature[::100]

    # Remove nan values
    salinity = salinity[~np.isnan(salinity)]
    temperature = temperature[~np.isnan(temperature)]

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
    sigma_theta = gsw.sigma0(salinity, temperature)

    return sigma_theta