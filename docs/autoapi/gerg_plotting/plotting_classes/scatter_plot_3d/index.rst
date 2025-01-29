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


   .. py:method:: add_bathy()


   .. py:method:: make_points_3d(x: str, y: str, z: str) -> numpy.ndarray

      A helper to make a 3D NumPy array of points (n_points by 3)



   .. py:method:: map(var: str | None = None) -> None


   .. py:method:: scatter(x: str, y: str, z: str, var: str | None = None) -> None


