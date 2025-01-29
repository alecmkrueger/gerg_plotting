gerg_plotting.plotting_classes.coverage_plot
============================================

.. py:module:: gerg_plotting.plotting_classes.coverage_plot


Classes
-------

.. autoapisummary::

   gerg_plotting.plotting_classes.coverage_plot.Base
   gerg_plotting.plotting_classes.coverage_plot.Coverage
   gerg_plotting.plotting_classes.coverage_plot.CoveragePlot
   gerg_plotting.plotting_classes.coverage_plot.ExtentArrows
   gerg_plotting.plotting_classes.coverage_plot.Grid


Module Contents
---------------

.. py:class:: Base

   Base class providing common functionality for attribute access and variable management.

   Methods
   -------
   _has_var(key)
       Check if object has a specific variable.
   get_vars()
       Get list of all object variables/attributes.
   __getitem__(key)
       Enable dictionary-style access to class attributes.
   __setitem__(key, value)
       Enable dictionary-style setting of class attributes.
   __str__()
       Return formatted string representation of class attributes.


   .. py:method:: get_vars() -> list

      Get list of all object variables/attributes.

      Returns
      -------
      list
          List of all variable names in the object.



.. py:class:: Coverage

   Bases: :py:obj:`Base`


   A class for creating and managing coverage representations including body, outline, label, and extent arrows.

   Parameters
   ----------
   body_min_height : float
       Minimum height for coverage body. Default is 0.25.
   body_alpha : float
       Transparency of coverage body. Default is 1.
   body_linewidth : float
       Line width of coverage body. Default is 1.
   body_color : str or tuple
       Fill color of coverage body. Default is 'none'.
   body_hatch : str
       Hatch pattern for coverage body. Default is None.
   body_hatch_color : str
       Color of hatch pattern. Default is None.
   hatch_linewidth : float
       Width of hatch lines. Default is 0.5.
   outline_edgecolor : str or tuple
       Color of outline. Default is 'k'.
   outline_alpha : float
       Transparency of outline. Default is 1.
   outline_linewidth : float
       Width of outline. Default is 1.
   label_fontsize : float
       Font size for label. Default is 12.
   label_background_pad : float
       Padding around label background. Default is 2.
   label_background_linewidth : float
       Width of label background border. Default is 0.
   label_background_alpha : float
       Transparency of label background. Default is 1.
   label_background_color : float
       Color of label background. Default is 'body_color'.
   show_arrows : bool
       Whether to show extent arrows. Default is True.

   Attributes
   ----------
   body : Rectangle
       The main coverage area rectangle.
   outline : Rectangle
       The outline rectangle.
   label : Text
       The coverage label.
   extent_arrows : ExtentArrows
       Arrows showing coverage extent.


   .. py:method:: add_label_background(text: matplotlib.text.Text)

      Add background to coverage label.

      Parameters
      ----------
      text : matplotlib.text.Text
          The text object to add background to.



   .. py:attribute:: body
      :type:  matplotlib.patches.Rectangle


   .. py:attribute:: body_alpha
      :type:  float


   .. py:attribute:: body_color
      :type:  str | tuple


   .. py:attribute:: body_hatch
      :type:  str


   .. py:attribute:: body_hatch_color
      :type:  str


   .. py:attribute:: body_linewidth
      :type:  float


   .. py:attribute:: body_min_height
      :type:  float


   .. py:method:: create(xrange, yrange, label, **kwargs)

      Create a new coverage object with specified range and label.

      Parameters
      ----------
      xrange : list
          Range of x-axis coverage [start, end].
      yrange : list
          Range of y-axis coverage [start, end].
      label : str
          Label text for the coverage.
      ``**kwargs``
          Additional keyword arguments for customizing appearance.

      Returns
      -------
      Coverage
          The created coverage object.



   .. py:attribute:: extent_arrows
      :type:  ExtentArrows


   .. py:attribute:: hatch_linewidth
      :type:  float


   .. py:attribute:: label
      :type:  matplotlib.text.Text


   .. py:attribute:: label_background_alpha
      :type:  float


   .. py:attribute:: label_background_color
      :type:  float


   .. py:attribute:: label_background_linewidth
      :type:  float


   .. py:attribute:: label_background_pad
      :type:  float


   .. py:attribute:: label_fontsize
      :type:  float


   .. py:attribute:: outline
      :type:  matplotlib.patches.Rectangle


   .. py:attribute:: outline_alpha
      :type:  float


   .. py:attribute:: outline_edgecolor
      :type:  str | tuple


   .. py:attribute:: outline_linewidth
      :type:  float


   .. py:method:: plot(ax: matplotlib.axes.Axes, **kwargs)

      Plot the coverage on given axes.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes to plot on.
      ``**kwargs``
          Additional keyword arguments for plotting.



   .. py:attribute:: show_arrows
      :type:  bool


.. py:class:: CoveragePlot

   Bases: :py:obj:`Base`


   A class for creating and managing plots showing multiple coverage areas.

   Parameters
   ----------
   fig : Figure, optional
       Matplotlib figure object.
   ax : Axes, optional
       Matplotlib axes object.
   figsize : tuple, optional
       Size of the figure (width, height).
   horizontal_padding : float
       Padding on left and right of plot. Default is 0.25.
   vertical_padding : float
       Padding on top and bottom of plot. Default is 0.75.
   xlabels : list
       Labels for x-axis ticks.
   ylabels : list
       Labels for y-axis ticks.
   cmap : str or Colormap
       Colormap for coverage areas.
   coverage_color_default : str or tuple
       Default color for coverages if specified.

   Attributes
   ----------
   color_iterator : itertools.cycle
       Iterator for cycling through colors.
   coverages : list
       List of Coverage objects.
   grid : Grid
       Grid object for the plot.
   plotting_kwargs : dict
       Default keyword arguments for plotting.


   .. py:method:: add_coverage(xrange, yrange, label=None, **kwargs)

      Add a new coverage area to the plot.

      Parameters
      ----------
      xrange : list or scalar
          Range or single value for x-axis coverage.
      yrange : list or scalar
          Range or single value for y-axis coverage.
      label : str, optional
          Label for the coverage area.
      ``**kwargs``
          Additional keyword arguments for coverage customization.

      Raises
      ------
      ValueError
          If xrange and yrange are not the same length.



   .. py:method:: add_grid(show_grid: bool)

      Add grid to the plot if requested.

      Parameters
      ----------
      show_grid : bool
          Whether to show the grid.



   .. py:attribute:: ax
      :type:  matplotlib.axes.Axes


   .. py:attribute:: cmap
      :type:  str | matplotlib.colors.Colormap


   .. py:attribute:: color_iterator
      :type:  itertools.cycle


   .. py:method:: coverage_color()

      Get the next color for a coverage area.

      Returns
      -------
      tuple or str
          RGBA color tuple or specified default color.



   .. py:attribute:: coverage_color_default


   .. py:attribute:: coverages
      :type:  list[Coverage]


   .. py:method:: custom_ticks(labels, axis: str)

      Set custom tick labels for specified axis.

      Parameters
      ----------
      labels : list
          List of tick labels.
      axis : str
          Axis to customize ('x' or 'y').



   .. py:attribute:: fig
      :type:  matplotlib.figure.Figure


   .. py:attribute:: figsize
      :type:  tuple


   .. py:attribute:: grid
      :type:  Grid


   .. py:method:: handle_ranges(xrange, yrange)

      Convert string labels to numeric indices for plotting.

      Parameters
      ----------
      xrange : list
          Range values for x-axis.
      yrange : list
          Range values for y-axis.

      Returns
      -------
      tuple
          Processed (xrange, yrange) with numeric values.



   .. py:attribute:: horizontal_padding
      :type:  float


   .. py:method:: init_figure() -> None

      Initialize figure and axes if not provided.



   .. py:method:: plot(show_grid=True)

      Create the complete coverage plot.

      Parameters
      ----------
      show_grid : bool, optional
          Whether to show grid lines. Default is True.



   .. py:method:: plot_coverages()

      Plot all coverage areas on the figure.



   .. py:attribute:: plotting_kwargs
      :type:  dict


   .. py:method:: save(filename, **kwargs)

      Save the current figure to a file.

      Parameters
      ----------
      filename : str
          Path to save the figure.
      ``**kwargs``
          Additional keyword arguments passed to savefig.

      Raises
      ------
      ValueError
          If no figure exists to save.



   .. py:method:: set_padding()

      Set plot limits with padding.



   .. py:method:: set_up_plot(show_grid: bool = True)

      Configure the plot with all necessary components.

      Parameters
      ----------
      show_grid : bool, optional
          Whether to show grid lines. Default is True.



   .. py:method:: show(**kwargs)

      Display the plot.

      Parameters
      ----------
      ``**kwargs``
          Additional keyword arguments passed to plt.show().



   .. py:attribute:: vertical_padding
      :type:  float


   .. py:attribute:: xlabels
      :type:  list


   .. py:attribute:: ylabels
      :type:  list


.. py:class:: ExtentArrows

   Bases: :py:obj:`Base`


   A class for managing and drawing arrows that indicate coverage extents.

   Parameters
   ----------
   arrow_facecolor : str or tuple
       Color of arrow fill. Use 'coverage_color' to match coverage color. Default is 'black'.
   arrow_edgecolor : str or tuple
       Color of arrow edges. Default is 'black'.
   arrow_tail_width : float
       Width of arrow tail. Default is 0.05.
   arrow_head_width : float
       Width of arrow head. Default is 0.12.
   arrow_zorder : float
       Z-order for arrow drawing. Default is 2.9.
   arrow_linewidth : float
       Width of arrow lines. Default is 0.
   arrow_text_padding : float
       Padding between arrow and text. Default is 0.05.

   Attributes
   ----------
   left_arrow : FancyArrow
       Arrow object for left extent.
   right_arrow : FancyArrow
       Arrow object for right extent.
   top_arrow : FancyArrow
       Arrow object for top extent.
   bottom_arrow : FancyArrow
       Arrow object for bottom extent.


   .. py:method:: add_range_arrows(ax: matplotlib.axes.Axes, text: matplotlib.text.Text, rect: matplotlib.patches.Rectangle)

      Add arrows indicating the range of coverage.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes to draw arrows on.
      text : matplotlib.text.Text
          Text object to position arrows around.
      rect : matplotlib.patches.Rectangle
          Rectangle representing coverage area.



   .. py:attribute:: arrow_edgecolor
      :type:  str | tuple


   .. py:attribute:: arrow_facecolor
      :type:  str | tuple


   .. py:attribute:: arrow_head_width
      :type:  float


   .. py:attribute:: arrow_linewidth
      :type:  float


   .. py:attribute:: arrow_tail_width
      :type:  float


   .. py:attribute:: arrow_text_padding
      :type:  float


   .. py:attribute:: arrow_zorder
      :type:  float


   .. py:attribute:: bottom_arrow
      :type:  matplotlib.patches.FancyArrow


   .. py:method:: calculate_arrow_length(ax: matplotlib.axes.Axes, rect, text_left, text_right)

      Calculate the lengths needed for extent arrows.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes containing the arrows.
      rect : Rectangle
          Rectangle object representing coverage area.
      text_left : float
          Left boundary of text.
      text_right : float
          Right boundary of text.

      Returns
      -------
      tuple
          (left_arrow_length, right_arrow_length)



   .. py:attribute:: left_arrow
      :type:  matplotlib.patches.FancyArrow


   .. py:attribute:: right_arrow
      :type:  matplotlib.patches.FancyArrow


   .. py:attribute:: top_arrow
      :type:  matplotlib.patches.FancyArrow


.. py:class:: Grid

   Bases: :py:obj:`Base`


   A class for managing and drawing grid lines on a plot.

   Parameters
   ----------
   xlabels : list
       Labels for x-axis grid lines.
   ylabels : list
       Labels for y-axis grid lines.
   grid_linewidth : float, optional
       Width of grid lines. Default is 1.
   grid_linestyle : str, optional
       Style of grid lines. Default is '--'.
   grid_color : str or tuple, optional
       Color of grid lines. Default is 'black'.
   grid_zorder : float, optional
       Z-order of grid lines. Default is 1.15.


   .. py:method:: add_grid(ax, **grid_kwargs)

      Add complete grid to the plot with both horizontal and vertical lines.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes to draw the grid on.
      ``**grid_kwargs``
          Additional keyword arguments for grid customization including:
          - grid_linewidth: Width of grid lines
          - grid_color: Color of grid lines
          - grid_linestyle: Style of grid lines



   .. py:method:: add_hlines(ax: matplotlib.axes.Axes, y_values, **kwargs)

      Add horizontal lines to the plot.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes to draw the lines on.
      y_values : array-like
          Y-coordinates where horizontal lines should be drawn.
      ``**kwargs``
          Additional keyword arguments passed to axhline.



   .. py:method:: add_vlines(ax: matplotlib.axes.Axes, x_values, **kwargs)

      Add vertical lines to the plot.

      Parameters
      ----------
      ax : matplotlib.axes.Axes
          The axes to draw the lines on.
      x_values : array-like
          X-coordinates where vertical lines should be drawn.
      ``**kwargs``
          Additional keyword arguments passed to axvline.



   .. py:attribute:: grid_color
      :type:  str | tuple


   .. py:attribute:: grid_linestyle
      :type:  str


   .. py:attribute:: grid_linewidth
      :type:  float


   .. py:attribute:: grid_zorder
      :type:  float


   .. py:attribute:: xlabels
      :type:  list


   .. py:attribute:: ylabels
      :type:  list


