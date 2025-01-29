gerg_plotting.modules.filters
=============================

.. py:module:: gerg_plotting.modules.filters


Functions
---------

.. autoapisummary::

   gerg_plotting.modules.filters.filter_nan
   gerg_plotting.modules.filters.filter_var


Module Contents
---------------

.. py:function:: filter_nan(values) -> numpy.ndarray

   Removes NaN values from an iterable or array-like object.

   Parameters:
       values (iterable): Input data (e.g., numpy array, pandas Series, xarray DataArray, list).

   Returns:
       Same type as input `values` with NaN values removed.


.. py:function:: filter_var(var, min_value, max_value) -> numpy.ndarray

   Filters values in an iterable or array-like object based on a range.

   Parameters:
       var (iterable): Input data (e.g., numpy array, pandas Series, xarray DataArray, list).
       min_value (float): Minimum threshold (inclusive).
       max_value (float): Maximum threshold (inclusive).

   Returns:
       Same type as input `var`, with values outside the range replaced by NaN


