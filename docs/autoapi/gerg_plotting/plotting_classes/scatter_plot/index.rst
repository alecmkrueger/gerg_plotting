gerg_plotting.plotting_classes.scatter_plot
===========================================

.. py:module:: gerg_plotting.plotting_classes.scatter_plot


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.scatter_plot.ScatterPlot


Module Contents
---------------

.. py:class:: ScatterPlot

   Bases: :py:obj:`gerg_plotting.plotting_classes.plotter.Plotter`


   Class for creating scatter plots from Data objects.

   Inherits from Plotter class for basic plotting functionality. Provides methods
   for various scatter plot types including T-S diagrams, hovmoller plots, and
   velocity vector plots.

   Parameters
   ----------
   markersize : int or float
       Size of scatter plot markers, default is 10


   .. py:method:: TS(color_var=None, fig=None, ax=None, contours: bool = True) -> None

      Create temperature-salinity diagram.

      Parameters
      ----------
      color_var : str or None, optional
          Variable name for color mapping
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      contours : bool, optional
          Whether to show sigma-theta contours, default True



   .. py:method:: calculate_quiver_step(num_points, quiver_density) -> int

      Calculate step size for quiver plot density.

      Parameters
      ----------
      num_points : int
          Total number of data points
      quiver_density : int
          Desired density of quiver arrows

      Returns
      -------
      int
          Step size for data sampling



   .. py:method:: cross_section(longitude, latitude) -> None
      :abstractmethod:


      Method placeholder for plotting cross-sections.

      Args:
          longitude: Longitude line for the cross-section.
          latitude: Latitude line for the cross-section.

      Raises:
          NotImplementedError: Indicates that the method is not yet implemented.



   .. py:method:: get_density_color_data(color_var: str) -> numpy.ndarray

      Get color data for density plotting.

      Parameters
      ----------
      color_var : str
          Variable name for color data

      Returns
      -------
      np.ndarray
          Array of color values



   .. py:method:: hovmoller(var: str, fig=None, ax=None, **kwargs) -> None

      Create depth vs time plot colored by variable.

      Parameters
      ----------
      var : str
          Variable name for color mapping
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      ``**kwargs``
          Additional arguments for scatter plot



   .. py:attribute:: markersize
      :type:  int | float


   .. py:method:: power_spectra_density(psd_freq=None, psd=None, var_name: str = None, sampling_freq=None, segment_length=None, theta_rad=None, highlight_freqs: list = None, fig=None, ax=None) -> None

      Create power spectral density plot.

      Parameters
      ----------
      psd_freq : array-like, optional
          Frequency values
      psd : array-like, optional
          Power spectral density values
      var_name : str, optional
          Variable name for PSD calculation
      sampling_freq : float, optional
          Sampling frequency
      segment_length : int, optional
          Length of segments for PSD calculation
      theta_rad : float, optional
          Angle in radians
      highlight_freqs : list, optional
          Frequencies to highlight
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on

      Raises
      ------
      ValueError
          If neither PSD values nor calculation parameters are provided



   .. py:method:: quiver1d(x: str, quiver_density: int = None, quiver_scale: float = None, fig=None, ax=None) -> None

      Create 1D quiver plot for velocity data.

      Parameters
      ----------
      x : str
          Variable name for x-axis
      quiver_density : int, optional
          Density of quiver arrows
      quiver_scale : float, optional
          Scaling factor for arrow length
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on



   .. py:method:: quiver2d(x: str, y: str, quiver_density: int = None, quiver_scale: float = None, fig=None, ax=None) -> None

      Create 2D quiver plot for velocity data.

      Parameters
      ----------
      x : str
          Variable name for x-axis
      y : str
          Variable name for y-axis
      quiver_density : int, optional
          Density of quiver arrows
      quiver_scale : float, optional
          Scaling factor for arrow length
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on



   .. py:method:: scatter(x: str, y: str, color_var: str | None = None, invert_yaxis: bool = False, fig=None, ax=None, **kwargs) -> None

      Create scatter plot of two variables with optional color mapping.

      Parameters
      ----------
      x : str
          Variable name for x-axis
      y : str
          Variable name for y-axis
      color_var : str or None, optional
          Variable name for color mapping
      invert_yaxis : bool, optional
          Whether to invert y-axis
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      ``**kwargs``
          Additional arguments for scatter plot

      Returns
      -------
      matplotlib.collections.PathCollection
          Scatter plot object



   .. py:method:: scatter3d(x: str, y: str, z: str, color_var: str | None = None, invert_yaxis: bool = False, fig=None, ax=None, **kwargs) -> None

      Create scatter plot of two variables with optional color mapping.

      Parameters
      ----------
      x : str
          Variable name for x-axis
      y : str
          Variable name for y-axis
      color_var : str or None, optional
          Variable name for color mapping
      invert_yaxis : bool, optional
          Whether to invert y-axis
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      ``**kwargs``
          Additional arguments for scatter plot

      Returns
      -------
      matplotlib.collections.PathCollection
          Scatter plot object



   .. py:method:: tricontourf(x: str, y: str, z: str, fig=None, ax=None, levels=None)

      Create filled contour plot of irregular grid data.

      Parameters
      ----------
      x : str
          Variable name for x-axis
      y : str
          Variable name for y-axis
      z : str
          Variable name for contour values
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      levels : int, optional
          Number of contour levels



