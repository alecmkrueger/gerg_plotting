gerg_plotting.plotting_classes.plotter_3d
=========================================

.. py:module:: gerg_plotting.plotting_classes.plotter_3d


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.plotter_3d.Plotter3D


Module Contents
---------------

.. py:class:: Plotter3D

   .. py:method:: add_colorbar(**kwargs)


   .. py:attribute:: bathy
      :type:  gerg_plotting.data_classes.bathy.Bathy


   .. py:method:: close()
      :abstractmethod:



   .. py:method:: convert_colormap(colormap, over_color=None, under_color=None) -> numpy.ndarray

      Convert colormap to uint8 color array.

      Parameters
      ----------
      colormap : Callable
          Function generating colors (matplotlib colormap)
      over_color : tuple, optional
          Color for highest value
      under_color : tuple, optional
          Color for lowest value

      Returns
      -------
      np.ndarray
          Array of RGBA colors scaled to 0-255



   .. py:attribute:: data
      :type:  gerg_plotting.data_classes.data.Data


   .. py:attribute:: figsize
      :type:  tuple


   .. py:method:: get_vars() -> list

      Get list of object attributes.

      Returns
      -------
      list
          List of attribute names



   .. py:method:: init_figure()


   .. py:attribute:: plotter
      :type:  pyvista.Plotter


   .. py:method:: save(filename, **kwargs)
      :abstractmethod:



   .. py:method:: show(**kwargs)


