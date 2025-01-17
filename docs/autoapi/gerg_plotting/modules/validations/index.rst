gerg_plotting.modules.validations
=================================

.. py:module:: gerg_plotting.modules.validations


Functions
---------

.. autoapisummary::

   gerg_plotting.modules.validations.is_flat_numpy_array
   gerg_plotting.modules.validations.lat_min_smaller_than_max
   gerg_plotting.modules.validations.lon_min_smaller_than_max


Module Contents
---------------

.. py:function:: is_flat_numpy_array(instance, attribute, value) -> None

   Validate that a value is a 1-dimensional NumPy array.

   Parameters
   ----------
   instance : object
       The class instance being validated
   attribute : attrs.Attribute
       The attribute being validated
   value : array_like
       The value to validate

   Raises
   ------
   ValueError
       If value is not a NumPy array or is not 1-dimensional


.. py:function:: lat_min_smaller_than_max(instance, attribute, value) -> None

   Validate that minimum latitude is smaller than maximum latitude.

   Parameters
   ----------
   instance : object
       The class instance being validated
   attribute : attrs.Attribute
       The attribute being validated
   value : float or None
       The value to validate

   Raises
   ------
   ValueError
       If lat_min is greater than or equal to lat_max


.. py:function:: lon_min_smaller_than_max(instance, attribute, value) -> None

   Validate that minimum longitude is smaller than maximum longitude.

   Parameters
   ----------
   instance : object
       The class instance being validated
   attribute : attrs.Attribute
       The attribute being validated
   value : float or None
       The value to validate

   Raises
   ------
   ValueError
       If lon_min is greater than or equal to lon_max


