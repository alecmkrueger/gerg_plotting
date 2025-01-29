gerg_plotting.plotting_classes.plotter
======================================

.. py:module:: gerg_plotting.plotting_classes.plotter


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.plotter.Plotter


Module Contents
---------------

.. py:class:: Plotter

   Base class for creating plots of data.

   Parameters
   ----------
   data : Data
       Data object containing variables to plot
   bounds_padding : float
       Padding to be applied to detected bounds
   fig : matplotlib.figure.Figure, optional
       Matplotlib figure object
   ax : matplotlib.axes.Axes, optional
       Matplotlib axes object
   nrows : int
       Number of rows in figure, default is 1
   cbar_nbins : int
       Number of bins for colorbar ticks, default is 5
   cbar_kwargs : dict
       Keyword arguments for colorbar customization

   Attributes
   ----------
   cbar : matplotlib.colorbar.Colorbar
       Colorbar object for the plot


   .. py:method:: add_colorbar(mappable: matplotlib.axes.Axes, var: str | None, divider=None, total_cbars: int = 2) -> None

      Add colorbar to plot.

      Parameters
      ----------
      mappable : matplotlib.axes.Axes
          Plot object to create colorbar for
      var : str or None
          Variable name for colorbar
      divider : optional
          Axes divider for colorbar positioning
      total_cbars : int, optional
          Total number of colorbars in plot, default 2

      Returns
      -------
      matplotlib.colorbar.Colorbar
          Created colorbar object



   .. py:method:: adjust_datetime_labels(rotation=30)

      Adjust datetime labels on x-axis to prevent overlap.

      Parameters
      ----------
      rotation : int, optional
          Rotation angle for labels if overlap detected, default 30



   .. py:attribute:: ax
      :type:  matplotlib.axes.Axes


   .. py:attribute:: bounds_padding
      :type:  float


   .. py:attribute:: cbar
      :type:  matplotlib.colorbar.Colorbar


   .. py:attribute:: cbar_kwargs
      :type:  dict


   .. py:attribute:: cbar_nbins
      :type:  int


   .. py:attribute:: data
      :type:  gerg_plotting.data_classes.data.Data


   .. py:attribute:: fig
      :type:  matplotlib.figure.Figure


   .. py:method:: format_axes(xlabel, ylabel, zlabel=None, invert_yaxis: bool = False) -> None

      Format plot axes with labels and options.

      Parameters
      ----------
      xlabel : str
          Label for x-axis
      ylabel : str
          Label for y-axis
      invert_yaxis : bool, optional
          Whether to invert y-axis, default False



   .. py:method:: get_cmap(color_var: str) -> matplotlib.colors.Colormap

      Get colormap for specified variable.

      Parameters
      ----------
      color_var : str
          Name of variable for colormap

      Returns
      -------
      matplotlib.colors.Colormap
          Colormap for variable



   .. py:method:: get_vars() -> list

      Get list of all object variables.

      Returns
      -------
      list
          List of variable names



   .. py:method:: init_figure(fig=None, ax=None, figsize=(6.4, 4.8), three_d=False, geography=False) -> None

      Initialize figure and axes objects.

      Parameters
      ----------
      fig : matplotlib.figure.Figure, optional
          Pre-existing figure
      ax : matplotlib.axes.Axes, optional
          Pre-existing axes
      figsize : tuple, optional
          Figure dimensions (width, height)
      three_d : bool, optional
          Whether to create 3D plot
      geography : bool, optional
          Whether to create map projection

      Raises
      ------
      ValueError
          If both three_d and geography are True



   .. py:attribute:: nrows
      :type:  int


   .. py:method:: save(filename, **kwargs)

      Save figure to file.

      Parameters
      ----------
      filename : str
          Path to save figure
      ``**kwargs``
          Additional arguments for savefig

      Raises
      ------
      ValueError
          If no figure exists



   .. py:method:: show()

      Show all open figures



