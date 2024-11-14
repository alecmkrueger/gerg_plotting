# calculations.py

import numpy as np
import gsw

def get_center_of_mass(lon, lat, pressure):
    return tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])


def get_sigma_theta(salinity, temperature, cnt=False):
    """
    Computes sigma_theta on a grid of temperature and salinity data.
    
    Args:
        salinity (np.ndarray): Array of salinity values.
        temperature (np.ndarray): Array of temperature values.
        cnt (bool): Whether to return a linear range of sigma_theta values.
    
    Returns:
        tuple: Meshgrid of salinity and temperature, calculated sigma_theta, 
               and optionally a linear range of sigma_theta values.
    """
    # Determine target sample size
    num_points = len(temperature)
    target_points = min(10_000, num_points)
    downsample_factor = max(1, num_points // target_points)

    # Downsample if necessary
    salinity = salinity[::downsample_factor]
    temperature = temperature[::downsample_factor]

    # Remove NaNs from the arrays
    salinity, temperature = salinity[~np.isnan(salinity)], temperature[~np.isnan(temperature)]

    # Calculate grid boundaries and mesh
    mint, maxt = np.min(temperature), np.max(temperature)
    mins, maxs = np.min(salinity), np.max(salinity)
    tempL, salL = np.linspace(mint - 1, maxt + 1, target_points), np.linspace(mins - 1, maxs + 1, target_points)
    Tg, Sg = np.meshgrid(tempL, salL)

    # Calculate density
    sigma_theta = gsw.sigma0(Sg, Tg)

    # Optionally, return a linear range of sigma_theta values
    return (Sg, Tg, sigma_theta, np.linspace(sigma_theta.min(), sigma_theta.max(), target_points)) if cnt else (Sg, Tg, sigma_theta)


def get_density(salinity, temperature):
    return gsw.sigma0(salinity, temperature)

def rotate_vector(u, v, theta_rad):
    u_rotated = u * np.cos(theta_rad) - v * np.sin(theta_rad)
    v_rotated = u * np.sin(theta_rad) + v * np.cos(theta_rad)
    return u_rotated, v_rotated
