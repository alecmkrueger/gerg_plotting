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

   Base class for 3D plotting using Mayavi.

   Parameters
   ----------
   data : Data
       Spatial data object containing coordinates and variables
   bathy : Bathy, optional
       Bathymetry data for depth visualization
   fig : mayavi.core.scene.Scene, optional
       Mayavi figure object
   figsize : tuple
       Size of figure window in pixels (width, height), default (1920, 1080)


   .. py:method:: add_colorbar(mappable, cmap_title, over_color=None, x_pos1_offset=None, y_pos1_offset=None, x_pos2_offset=None, y_pos2_offset=None, cmap=None)

      Add colorbar to 3D plot.

      Parameters
      ----------
      mappable : mayavi.modules.glyph.Glyph
          3D plot object
      cmap_title : str
          Title for colorbar
      over_color : tuple, optional
          Color for highest value
      x_pos1_offset : float, optional
          X offset for position
      y_pos1_offset : float, optional
          Y offset for position
      x_pos2_offset : float, optional
          X offset for position2
      y_pos2_offset : float, optional
          Y offset for position2
      cmap : Callable, optional
          Custom colormap function

      Returns
      -------
      mayavi.modules.scalarbar.ScalarBar
          Created colorbar



   .. py:attribute:: bathy
      :type:  gerg_plotting.data_classes.bathy.Bathy


   .. py:method:: close()

      Close the Mayavi window.



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


   .. py:attribute:: fig
      :type:  mayavi.core.scene.Scene


   .. py:attribute:: figsize
      :type:  tuple


   .. py:method:: format_colorbar(colorbar, x_pos1_offset, y_pos1_offset, x_pos2_offset, y_pos2_offset)

      Format colorbar appearance.

      Parameters
      ----------
      colorbar : mayavi.modules.scalarbar.ScalarBar
          Colorbar to format
      x_pos1_offset : float
          X offset for position
      y_pos1_offset : float
          Y offset for position
      x_pos2_offset : float
          X offset for position2
      y_pos2_offset : float
          Y offset for position2

      Returns
      -------
      mayavi.modules.scalarbar.ScalarBar
          Formatted colorbar



   .. py:method:: get_vars() -> list

      Get list of object attributes.

      Returns
      -------
      list
          List of attribute names



   .. py:method:: init_figure(fig=None)

      Initialize Mayavi figure.

      Parameters
      ----------
      fig : mayavi.core.scene.Scene, optional
          Existing figure to use

      Returns
      -------
      mayavi.core.scene.Scene
          Initialized figure for plotting

      Raises
      ------
      ValueError
          If fig is not None or a mayavi.core.scene.Scene object



   .. py:method:: save(filename, size=None, **kwargs)

      Save the 3D scene to file.

      Must be called before show() with show=False in plotting method.

      Parameters
      ----------
      filename : str
          Output filename
      size : tuple, optional
          Image size in pixels
      ``**kwargs``
          Additional arguments for scene.save()

      Raises
      ------
      ValueError
          If no scene exists



   .. py:method:: show()

      Display the 3D plot in Mayavi window.



