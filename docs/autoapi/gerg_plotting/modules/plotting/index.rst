gerg_plotting.modules.plotting
==============================

.. py:module:: gerg_plotting.modules.plotting


Functions
---------

.. autoapisummary::

   gerg_plotting.modules.plotting.colorbar
   gerg_plotting.modules.plotting.get_turner_cmap


Module Contents
---------------

.. py:function:: colorbar(fig, divider, mappable, label, nrows=1, total_cbars=2) -> matplotlib.colorbar.Colorbar

   Create a colorbar with automatic positioning for multiple subplots.

   Parameters
   ----------
   fig : matplotlib.figure.Figure
       The figure object to add the colorbar to
   divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider
       Divider object for positioning the colorbar
   mappable : matplotlib.cm.ScalarMappable
       The mappable object to create the colorbar from
   label : str
       Label for the colorbar
   nrows : int, optional
       Number of rows in the subplot grid, default is 1
   total_cbars : int, optional
       Total number of colorbars expected, default is 2

   Returns
   -------
   matplotlib.colorbar.Colorbar
       The created colorbar object


.. py:function:: get_turner_cmap() -> matplotlib.colors.ListedColormap

   Create a custom colormap for Turner angle visualization.

   Creates a colormap with distinct regions for different Turner angle ranges:
   - Red (0-45°)
   - Yellow (45-135°)
   - Green (135-225°)
   - Blue (225-315°)
   - Red (315-360°)

   Returns
   -------
   matplotlib.colors.ListedColormap
       Custom colormap for Turner angle visualization with 256 colors


