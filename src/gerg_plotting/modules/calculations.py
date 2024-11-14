# calculations.py

import numpy as np
import gsw

def get_center_of_mass(lon, lat, pressure):
    return tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])

def get_sigma_theta(salinity, temperature, cnt=False):
    num_points = len(temperature)
    if 50_000 < num_points < 300_000:
        salinity, temperature = salinity[::100], temperature[::100]
    elif 300_000 < num_points < 1_000_000:
        salinity, temperature = salinity[::250], temperature[::250]
    elif num_points >= 1_000_000:
        salinity, temperature = salinity[::1000], temperature[::1000]

    salinity, temperature = salinity[~np.isnan(salinity)], temperature[~np.isnan(temperature)]
    mint, maxt = np.min(temperature), np.max(temperature)
    mins, maxs = np.min(salinity), np.max(salinity)
    tempL, salL = np.linspace(mint - 1, maxt + 1, num_points), np.linspace(mins - 1, maxs + 1, num_points)
    Tg, Sg = np.meshgrid(tempL, salL)
    sigma_theta = gsw.sigma0(Sg, Tg)
    
    return (Sg, Tg, sigma_theta, np.linspace(sigma_theta.min(), sigma_theta.max(), num_points)) if cnt else (Sg, Tg, sigma_theta)

def get_density(salinity, temperature):
    return gsw.sigma0(salinity, temperature)

def rotate_vector(u, v, theta_rad):
    u_rotated = u * np.cos(theta_rad) - v * np.sin(theta_rad)
    v_rotated = u * np.sin(theta_rad) + v * np.cos(theta_rad)
    return u_rotated, v_rotated
