gerg_plotting.data_classes.bathy
================================

.. py:module:: gerg_plotting.data_classes.bathy


Classes
-------

.. autoapisummary::

   gerg_plotting.data_classes.bathy.Bathy


Module Contents
---------------

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


