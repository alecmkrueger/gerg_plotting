gerg_plotting.plotting_classes.scatter_plot_3d
==============================================

.. py:module:: gerg_plotting.plotting_classes.scatter_plot_3d


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.scatter_plot_3d.ScatterPlot3D


Module Contents
---------------

.. py:class:: ScatterPlot3D

   Bases: :py:obj:`gerg_plotting.plotting_classes.plotter_3d.Plotter3D`


   Class for creating 3D scatter plots using Mayavi.

   Inherits from Plotter3D to provide advanced 3D visualization capabilities
   with optional bathymetric data and variable-based color mapping.


   .. py:method:: map(var: str | None = None, point_size: int | float = 0.05, bounds_padding=0, vertical_scalar=None, fig=None, show: bool = True) -> None

      Create 3D map with bathymetry and scatter points.

      Parameters
      ----------
      var : str or None, optional
          Variable name for color mapping
      point_size : int or float, optional
          Size of scatter points, default 0.05
      bounds_padding : float, optional
          Padding for map bounds, default 0
      vertical_scalar : float, optional
          Scaling factor for depth values
      fig : mayavi.core.scene.Scene, optional
          Figure to plot on
      show : bool, optional
          Whether to display plot, default True



   .. py:method:: scatter(var: str | None = None, point_size: int | float = 0.05, vertical_scalar=None, fig=None, show: bool = True) -> None

      Create 3D scatter plot.

      Parameters
      ----------
      var : str or None, optional
          Variable name for color mapping
      point_size : int or float, optional
          Size of scatter points, default 0.05
      vertical_scalar : float, optional
          Scaling factor for depth values
      fig : mayavi.core.scene.Scene, optional
          Figure to plot on
      show : bool, optional
          Whether to display plot, default True



