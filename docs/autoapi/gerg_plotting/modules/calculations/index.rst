gerg_plotting.modules.calculations
==================================

.. py:module:: gerg_plotting.modules.calculations


Functions
---------

.. autoapisummary::

   gerg_plotting.modules.calculations.get_center_of_mass
   gerg_plotting.modules.calculations.get_density
   gerg_plotting.modules.calculations.get_sigma_theta
   gerg_plotting.modules.calculations.rotate_vector


Module Contents
---------------

.. py:function:: get_center_of_mass(lon: numpy.ndarray, lat: numpy.ndarray, pressure: numpy.ndarray) -> tuple

   Calculates the center of mass for given longitude, latitude, and pressure arrays.
   Handles cases where inputs are empty or contain only NaN values.

   Parameters:
   - lon (np.ndarray): Array of longitude values.
   - lat (np.ndarray): Array of latitude values.
   - pressure (np.ndarray): Array of pressure values.

   Returns:
   - tuple: A tuple containing the mean longitude, mean latitude, and mean pressure. If an input is empty or all-NaN, the corresponding value in the tuple is np.nan.


.. py:function:: get_density(salinity, temperature) -> numpy.ndarray

   Calculate seawater density (sigma-0) from salinity and temperature.

   Parameters
   ----------
   salinity : array_like
       Practical salinity [PSU]
   temperature : array_like
       Temperature [°C]

   Returns
   -------
   np.ndarray
       Potential density [kg/m³] referenced to 0 dbar pressure


.. py:function:: get_sigma_theta(salinity, temperature, cnt=False) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray] | tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]

   Computes sigma_theta on a grid of temperature and salinity data.

   Args:
       salinity (np.ndarray): Array of salinity values.
       temperature (np.ndarray): Array of temperature values.
       cnt (bool): Whether to return a linear range of sigma_theta values.

   Returns:
       tuple: Meshgrid of salinity and temperature, calculated sigma_theta, 
              and optionally a linear range of sigma_theta values.


.. py:function:: rotate_vector(u, v, theta_rad) -> tuple[numpy.ndarray, numpy.ndarray]

   Rotate velocity vectors by a given angle.

   Parameters
   ----------
   u : array_like
       Zonal (east-west) velocity component
   v : array_like
       Meridional (north-south) velocity component
   theta_rad : float
       Rotation angle in radians

   Returns
   -------
   tuple[np.ndarray, np.ndarray]
       Rotated u and v components (u_rotated, v_rotated)


