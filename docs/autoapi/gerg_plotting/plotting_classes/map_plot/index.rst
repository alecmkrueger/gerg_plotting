gerg_plotting.plotting_classes.map_plot
=======================================

.. py:module:: gerg_plotting.plotting_classes.map_plot


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.map_plot.MapPlot


Module Contents
---------------

.. py:class:: MapPlot

   Bases: :py:obj:`gerg_plotting.plotting_classes.plotter.Plotter`


   A class for plotting geographic data on maps using Cartopy and Matplotlib.

   Parameters
   ----------
   bathy : Bathy, optional
       Bathymetric data object
   grid_spacing : int, optional
       Spacing between gridlines in degrees, default is 1

   Attributes
   ----------
   sc : matplotlib.collections.PathCollection
       Scatter plot collection
   gl : cartopy.mpl.gridliner.Gridliner
       Gridliner for map coordinates
   cbar_var : matplotlib.colorbar.Colorbar
       Colorbar for plotted variable
   cbar_bathy : matplotlib.colorbar.Colorbar
       Colorbar for bathymetry


   .. py:method:: add_bathy(show_bathy, divider) -> None

      Add bathymetric contours to map.

      Parameters
      ----------
      show_bathy : bool
          Whether to display bathymetry
      divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider
          Divider for colorbar placement



   .. py:method:: add_coasts(show_coastlines) -> None

      Add coastlines to the map.

      Parameters
      ----------
      show_coastlines : bool
          Whether to display coastlines



   .. py:method:: add_grid(grid: bool, show_coords: bool = True) -> None

      Add gridlines and coordinate labels to map.

      Parameters
      ----------
      grid : bool
          Whether to show gridlines
      show_coords : bool, optional
          Whether to show coordinate labels, default True



   .. py:attribute:: bathy
      :type:  gerg_plotting.data_classes.bathy.Bathy


   .. py:attribute:: cbar_bathy
      :type:  matplotlib.colorbar.Colorbar


   .. py:attribute:: cbar_var
      :type:  matplotlib.colorbar.Colorbar


   .. py:method:: get_quiver_step(quiver_density) -> int | None

      Calculate step size for quiver plot density.

      Parameters
      ----------
      quiver_density : int or None
          Desired density of quiver arrows

      Returns
      -------
      int or None
          Step size for data slicing



   .. py:attribute:: gl
      :type:  cartopy.mpl.gridliner.Gridliner


   .. py:attribute:: grid_spacing
      :type:  int


   .. py:method:: init_bathy() -> None

      Initialize bathymetry object based on map bounds.

      Creates a new Bathy object if none exists, using current map bounds.



   .. py:method:: quiver(x: str = 'lon', y: str = 'lat', quiver_density: int = None, quiver_scale: float = None, grid: bool = True, show_bathy: bool = True, show_coastlines: bool = True, fig=None, ax=None) -> None

      Create quiver plot for vector data.

      Parameters
      ----------
      x : str, optional
          X-axis variable name, default 'lon'
      y : str, optional
          Y-axis variable name, default 'lat'
      quiver_density : int, optional
          Density of quiver arrows
      quiver_scale : float, optional
          Scaling factor for arrow length
      grid : bool, optional
          Whether to show grid, default True
      show_bathy : bool, optional
          Whether to show bathymetry, default True
      show_coastlines : bool, optional
          Whether to show coastlines, default True
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on



   .. py:attribute:: sc
      :type:  matplotlib.collections.PathCollection


   .. py:method:: scatter(var: str | None = None, show_bathy: bool = True, show_coastlines: bool = True, pointsize=3, linewidths=0, grid=True, show_coords=True, fig=None, ax=None) -> None

      Create scatter plot of points on map.

      Parameters
      ----------
      var : str or None, optional
          Variable name for color mapping
      show_bathy : bool, optional
          Whether to show bathymetry, default True
      show_coastlines : bool, optional
          Whether to show coastlines, default True
      pointsize : int, optional
          Size of scatter points, default 3
      linewidths : int, optional
          Width of point edges, default 0
      grid : bool, optional
          Whether to show grid, default True
      show_coords : bool, optional
          Whether to show coordinates, default True
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on



   .. py:method:: set_up_map(fig=None, ax=None, var=None) -> tuple[str, matplotlib.colors.Colormap, mpl_toolkits.axes_grid1.axes_divider.AxesDivider] | tuple[numpy.ndarray, matplotlib.colors.Colormap, mpl_toolkits.axes_grid1.axes_divider.AxesDivider]

      Set up the base map with figure, axes, and color settings.

      Parameters
      ----------
      fig : matplotlib.figure.Figure, optional
          Figure to plot on
      ax : matplotlib.axes.Axes, optional
          Axes to plot on
      var : str, optional
          Variable name for color mapping

      Returns
      -------
      tuple
          (color, cmap, divider)
          - color : str or ndarray, Color values for plotting
          - cmap : matplotlib.colors.Colormap, Colormap for variable
          - divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider, Divider for colorbar placement



