gerg_plotting.plotting_classes.histogram
========================================

.. py:module:: gerg_plotting.plotting_classes.histogram


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.histogram.Histogram


Module Contents
---------------

.. py:class:: Histogram

   Bases: :py:obj:`gerg_plotting.plotting_classes.plotter.Plotter`


   A class for plotting histograms from instrument data using matplotlib.

   This class provides methods for creating 1D, 2D, and 3D histograms from data.
   Inherits from Plotter class for basic plotting functionality.


   .. py:method:: get_2d_range(x: str, y: str, **kwargs) -> tuple[list, dict]

      Calculate or retrieve the range for 2D histograms.

      Parameters
      ----------
      x : str
          Name of the x-axis variable
      y : str
          Name of the y-axis variable
      ``**kwargs`` : dict
          Optional keyword arguments including 'range' for custom ranges

      Returns
      -------
      tuple
          (range_list, modified_kwargs)
          - range_list : calculated or provided range values
          - modified_kwargs : kwargs with 'range' removed if present



   .. py:method:: plot(var: str, fig=None, ax=None, **kwargs) -> None

      Plot a 1D histogram of the given variable.

      Parameters
      ----------
      var : str
          Name of the variable to plot
      fig : matplotlib.figure.Figure, optional
          Figure object to use for plotting
      ax : matplotlib.axes.Axes, optional
          Axes object to use for plotting
      ``**kwargs`` : dict
          Additional keyword arguments passed to matplotlib.pyplot.hist



   .. py:method:: plot2d(x: str, y: str, fig=None, ax=None, **kwargs) -> None

      Plot a 2D histogram for the x and y variables.

      Parameters
      ----------
      x : str
          Name of the x-axis variable
      y : str
          Name of the y-axis variable
      fig : matplotlib.figure.Figure, optional
          Figure object to use for plotting
      ax : matplotlib.axes.Axes, optional
          Axes object to use for plotting
      ``**kwargs`` : dict
          Additional keyword arguments passed to matplotlib.pyplot.hist2d



   .. py:method:: plot3d(x: str, y: str, fig=None, ax=None, **kwargs) -> None

      Plot a 3D surface plot based on a 2D histogram.

      Parameters
      ----------
      x : str
          Name of the x-axis variable
      y : str
          Name of the y-axis variable
      fig : matplotlib.figure.Figure, optional
          Figure object to use for plotting
      ax : matplotlib.axes.Axes, optional
          Axes object to use for plotting
      ``**kwargs`` : dict
          Additional keyword arguments passed to numpy.histogram2d



