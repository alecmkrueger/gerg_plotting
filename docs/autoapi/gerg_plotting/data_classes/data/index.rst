gerg_plotting.data_classes.data
===============================

.. py:module:: gerg_plotting.data_classes.data


Classes
-------

.. autoapisummary::

   gerg_plotting.data_classes.data.Data


Module Contents
---------------

.. py:class:: Data

   Represents a spatial dataset with various oceanographic or atmospheric variables.

   Attributes
   ----------
   lat : Iterable | Variable | None
       Latitude values or Variable object containing latitude data
   lon : Iterable | Variable | None
       Longitude values or Variable object containing longitude data
   depth : Iterable | Variable | None
       Depth values or Variable object containing depth data
   time : Iterable | Variable | None
       Time values or Variable object containing temporal data
   bounds : Bounds, optional
       Geographic and depth bounds for the dataset
   custom_variables : dict
       Dictionary to store additional custom variables
   temperature : Iterable, Variable, or None, optional
       Temperature data, in °C, with optional colormap and range specifications.
   salinity : Iterable, Variable, or None, optional
       Salinity data with optional colormap and range specifications.
   density : Iterable, Variable, or None, optional
       Density data, in kg/m³, with optional colormap and range specifications.
   u : Iterable, Variable, or None, optional
       Zonal velocity (u-component) in m/s, with optional colormap and range specifications.
   v : Iterable, Variable, or None, optional
       Meridional velocity (v-component) in m/s, with optional colormap and range specifications.
   w : Iterable, Variable, or None, optional
       Vertical velocity (w-component) in m/s, with optional colormap and range specifications.
   speed : Iterable, Variable, or None, optional
       Speed data, derived or directly assigned, in m/s, with optional colormap and range specifications.
   chlor : Iterable, Variable, or None, optional
       Chlorophyll data, in μg/L, with optional colormap and range specifications.
   cdom : Iterable, Variable, or None, optional
       CDOM data, in ppb, with optional colormap and range specifications.
   turbidity : Iterable, Variable, or None, optional
       Turbidity data, dimensionless, with optional colormap and range specifications.
   bounds : Bounds
       Spatial bounds of the data.


   .. py:method:: add_custom_variable(variable: gerg_plotting.data_classes.variable.Variable, exist_ok: bool = False) -> None

      Add a custom Variable object accessible via both dot and dict syntax.

      Parameters
      ----------
      variable : Variable
          The Variable object to add
      exist_ok : bool, optional
          If True, replace existing variable if it exists, by default False

      Raises
      ------
      TypeError
          If provided object is not a Variable instance
      AttributeError
          If variable name already exists and exist_ok is False



   .. py:attribute:: bounds
      :type:  gerg_plotting.data_classes.bounds.Bounds


   .. py:method:: calcluate_PSD(sampling_freq, segment_length, theta_rad=None) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray] | tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]

      Calculate the power spectral density (PSD) using Welch's method.

      Parameters
      ----------
      sampling_freq : float
          Sampling frequency of the data in Hz.
      segment_length : int
          Length of each segment for Welch's method.
      theta_rad : float, optional
          Angle of rotation in radians. Rotates the u and v components if specified.

      Returns
      -------
      tuple
          A tuple containing the frequency array and PSD values for the velocity components.
          If the vertical component (w) is available, it is also included in the tuple.



   .. py:method:: calculate_speed(include_w: bool = False) -> None

      Calculate the speed from velocity components.

      Parameters
      ----------
      include_w : bool, optional
          If True, includes the vertical velocity (w-component) in the speed calculation.
          Defaults to False.



   .. py:attribute:: cdom
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: check_for_vars(vars: list) -> bool

      Verify that all required variables exist in the dataset.

      Parameters
      ----------
      vars : list
          List of variable names to check

      Returns
      -------
      bool
          True if all variables exist

      Raises
      ------
      ValueError
          If any required variables are missing



   .. py:attribute:: chlor
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: copy()

      Creates a deep copy of the instrument object.



   .. py:attribute:: custom_variables
      :type:  dict


   .. py:method:: date2num() -> list

      Converts time data to numerical values.



   .. py:attribute:: density
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: depth
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: detect_bounds(bounds_padding=0) -> gerg_plotting.data_classes.bounds.Bounds

      Detect the geographic bounds of the data, applying padding if specified.

      An intentional effect of this function:
          will only calculate the bounds when self.bounds is None,
          so that it does not overwrite the user's custom bounds,
          this will also ensure that the bounds is not repeatedly calculated unless desired,
          can recalculate self.bounds using a new bounds_padding value if self.bounds is set to None

      The depth bounds are not affected by the bounds padding, therfore the max and min values of the depth data are used

      Parameters
      ----------
      bounds_padding : float, optional
          Padding to add to the detected bounds, by default 0

      Returns
      -------
      Bounds
          Object containing the detected geographic and depth bounds




   .. py:method:: get_vars(have_data: bool | None = None) -> list

      Gets a list of all available variables.



   .. py:attribute:: lat
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: lon
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: remove_custom_variable(variable_name) -> None

      Remove a custom variable from the instrument.

      Parameters
      ----------
      variable_name : str
          Name of the variable to remove



   .. py:attribute:: salinity
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: slice_var(var: str, slice: Data.slice_var.slice) -> numpy.ndarray

      Slices data for a specific variable.



   .. py:attribute:: speed
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: temperature
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: time
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: turbidity
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: u
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: v
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: w
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


