gerg_plotting.data_classes
==========================

.. py:module:: gerg_plotting.data_classes


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/gerg_plotting/data_classes/bathy/index
   /autoapi/gerg_plotting/data_classes/bounds/index
   /autoapi/gerg_plotting/data_classes/data/index
   /autoapi/gerg_plotting/data_classes/variable/index


Classes
-------

.. autoapisummary::

   gerg_plotting.data_classes.Bathy
   gerg_plotting.data_classes.Bounds
   gerg_plotting.data_classes.Data
   gerg_plotting.data_classes.Variable


Package Contents
----------------

.. py:class:: Bathy

   Bathy class for handling bathymetry data and visualization.

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
   bounds : Bounds
       Object containing spatial and vertical boundaries for the dataset.
   resolution_level : float or int, optional
       Degree resolution for coarsening the dataset, default is 5.
   contour_levels : int, optional
       Number of contour levels for visualization, default is 50.
   land_color : list
       RGBA color values for representing land, default is [231/255, 194/255, 139/255, 1].
   vmin : float or int, optional
       Minimum value for the colormap, default is 0.
   cmap : Colormap
       Colormap for bathymetry visualization, default is 'Blues'.
   cbar_show : bool
       Whether to display a colorbar, default is True.
   cbar : matplotlib.colorbar.Colorbar
       Colorbar for the bathymetry visualization.
   cbar_nbins : int
       Number of bins for colorbar ticks, default is 5.
   cbar_kwargs : dict
       Additional keyword arguments for the colorbar.
   center_of_mass : tuple
       Center of mass of the bathymetry data (longitude, latitude, depth).
   label : str
       Label for the bathymetry data, default is 'Bathymetry'.


   .. py:method:: add_colorbar(fig: matplotlib.figure.Figure, divider, mappable: matplotlib.axes.Axes, nrows: int) -> None

      Add a colorbar to the figure.

      Parameters
      ----------
      fig : matplotlib.figure.Figure
          The figure to which the colorbar is added.
      divider : AxesDivider
          Divider to place the colorbar appropriately.
      mappable : matplotlib.axes.Axes
          The mappable object (e.g., image or contour plot).
      nrows : int
          Number of rows in the figure layout.

      Returns
      -------
      matplotlib.colorbar.Colorbar
          The created colorbar instance.



   .. py:method:: adjust_cmap() -> None

      Adjust the colormap by cropping and adding land color.



   .. py:attribute:: bounds
      :type:  gerg_plotting.data_classes.bounds.Bounds


   .. py:attribute:: cbar
      :type:  matplotlib.colorbar.Colorbar


   .. py:attribute:: cbar_kwargs
      :type:  dict


   .. py:attribute:: cbar_nbins
      :type:  int


   .. py:attribute:: cbar_show
      :type:  bool


   .. py:attribute:: center_of_mass
      :type:  tuple


   .. py:attribute:: cmap
      :type:  matplotlib.colors.Colormap


   .. py:attribute:: contour_levels
      :type:  int


   .. py:method:: copy()

      Creates a deep copy of the instrument object.



   .. py:attribute:: depth
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:method:: get_bathy() -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]

      Load and process bathymetry data.

      Returns
      -------
      tuple of np.ndarray
          Longitude, latitude, and depth values.

      Raises
      ------
      ValueError
          If the bounds attribute is not provided.



   .. py:method:: get_label() -> str

      Get the label for the bathymetry data, including units if provided.

      Returns
      -------
      str
          Label for the bathymetry data.



   .. py:method:: get_vars() -> list

      Gets a list of all available variables.



   .. py:attribute:: label
      :type:  str


   .. py:attribute:: land_color
      :type:  list


   .. py:attribute:: lat
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: lon
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: resolution_level
      :type:  float | int | None


   .. py:attribute:: time
      :type:  Iterable | gerg_plotting.data_classes.variable.Variable | None


   .. py:attribute:: vmin
      :type:  int | float


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


.. py:class:: Variable

   A class representing a scientific variable with its data and visualization properties.

   This class handles data arrays along with their metadata and visualization settings,
   providing methods for data access and label generation.

   Parameters
   ----------
   data : np.ndarray
       The numerical data for the variable
   name : str
       Name identifier for the variable
   cmap : Colormap, optional
       Matplotlib colormap for visualization
   units : str, optional
       Units of measurement
   vmin : float, optional
       Minimum value for visualization scaling
   vmax : float, optional
       Maximum value for visualization scaling
   label : str, optional
       Custom label for plotting

   Attributes
   ----------
   data : np.ndarray
       Flat numpy array containing the variable data
   name : str
       Variable name identifier
   cmap : Colormap
       Colormap for visualization
   units : str
       Units of measurement
   vmin : float
       Minimum value for visualization
   vmax : float
       Maximum value for visualization
   label : str
       Display label for plots


   .. py:attribute:: cmap
      :type:  matplotlib.colors.Colormap


   .. py:attribute:: data
      :type:  numpy.ndarray


   .. py:method:: get_attrs() -> list

      Get list of all attributes for the variable.

      Returns
      -------
      list
          List of attribute names



   .. py:method:: get_label() -> str

      Generate a formatted label for the variable.

      Returns
      -------
      str
          Formatted label including variable name and units if available



   .. py:method:: get_vmin_vmax(ignore_existing: bool = False) -> None

      Calculate or update the minimum and maximum values for visualization.

      Uses 1st and 99th percentiles of the data to set visualization bounds,
      excluding time variables.

      Parameters
      ----------
      ignore_existing : bool, optional
          If True, recalculate bounds even if they exist



   .. py:attribute:: label
      :type:  str


   .. py:attribute:: name
      :type:  str


   .. py:method:: reset_label() -> None

      Reset the label to the variable name.



   .. py:attribute:: units
      :type:  str


   .. py:attribute:: vmax
      :type:  float


   .. py:attribute:: vmin
      :type:  float


