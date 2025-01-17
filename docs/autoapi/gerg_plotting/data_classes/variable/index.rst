gerg_plotting.data_classes.variable
===================================

.. py:module:: gerg_plotting.data_classes.variable


Classes
-------

.. autoapisummary::

   gerg_plotting.data_classes.variable.Variable


Module Contents
---------------

.. py:class:: Variable

   A class representing a scientific variable with its data and visualization properties.

   This class handles data arrays along with their metadata and visualization settings,
   providing methods for data access and label generation.

   Parameters
   ----------
   data : np.ndarray
       The numerical data for the variable
   name : str
       Name identifier for the variable
   cmap : Colormap, optional
       Matplotlib colormap for visualization
   units : str, optional
       Units of measurement
   vmin : float, optional
       Minimum value for visualization scaling
   vmax : float, optional
       Maximum value for visualization scaling
   label : str, optional
       Custom label for plotting

   Attributes
   ----------
   data : np.ndarray
       Flat numpy array containing the variable data
   name : str
       Variable name identifier
   cmap : Colormap
       Colormap for visualization
   units : str
       Units of measurement
   vmin : float
       Minimum value for visualization
   vmax : float
       Maximum value for visualization
   label : str
       Display label for plots


   .. py:attribute:: cmap
      :type:  matplotlib.colors.Colormap


   .. py:attribute:: data
      :type:  numpy.ndarray


   .. py:method:: get_attrs() -> list

      Get list of all attributes for the variable.

      Returns
      -------
      list
          List of attribute names



   .. py:method:: get_label() -> str

      Generate a formatted label for the variable.

      Returns
      -------
      str
          Formatted label including variable name and units if available



   .. py:method:: get_vmin_vmax(ignore_existing: bool = False) -> None

      Calculate or update the minimum and maximum values for visualization.

      Uses 1st and 99th percentiles of the data to set visualization bounds,
      excluding time variables.

      Parameters
      ----------
      ignore_existing : bool, optional
          If True, recalculate bounds even if they exist



   .. py:attribute:: label
      :type:  str


   .. py:attribute:: name
      :type:  str


   .. py:method:: reset_label() -> None

      Reset the label to the variable name.



   .. py:attribute:: units
      :type:  str


   .. py:attribute:: vmax
      :type:  float


   .. py:attribute:: vmin
      :type:  float


