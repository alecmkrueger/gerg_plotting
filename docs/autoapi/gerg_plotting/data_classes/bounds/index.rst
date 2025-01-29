gerg_plotting.data_classes.bounds
=================================

.. py:module:: gerg_plotting.data_classes.bounds


Classes
-------

.. autoapisummary::

   gerg_plotting.data_classes.bounds.Bounds


Module Contents
---------------

.. py:class:: Bounds

   Represents geographic and depth bounds for a spatial dataset.

   Attributes
   ----------
   lat_min : float | int | None
       Minimum latitude of the bounds. Must be smaller than `lat_max`.
   lat_max : float | int | None
       Maximum latitude of the bounds.
   lon_min : float | int | None
       Minimum longitude of the bounds. Must be smaller than `lon_max`.
   lon_max : float | int | None
       Maximum longitude of the bounds.
   depth_bottom : float | int | None
       Maximum depth value (positive, in meters). Represents the bottom of the range.
   depth_top : float | int | None
       Minimum depth value (positive, in meters). Represents the top of the range (e.g., surface).
   vertical_scalar : float | int | None
       A scaling factor applied to depth values. Default is 1.
   vertical_units : str | None
       Units for the vertical depth values. Default is "m".


   .. py:attribute:: depth_bottom
      :type:  float | int | None


   .. py:attribute:: depth_top
      :type:  float | int | None


   .. py:attribute:: lat_max
      :type:  float | int | None


   .. py:attribute:: lat_min
      :type:  float | int | None


   .. py:attribute:: lon_max
      :type:  float | int | None


   .. py:attribute:: lon_min
      :type:  float | int | None


   .. py:attribute:: vertical_scalar
      :type:  float | int | None


   .. py:attribute:: vertical_units
      :type:  str | None


