gerg_plotting.modules.utilities
===============================

.. py:module:: gerg_plotting.modules.utilities


Functions
---------

.. autoapisummary::

   gerg_plotting.modules.utilities.calculate_pad
   gerg_plotting.modules.utilities.calculate_range
   gerg_plotting.modules.utilities.extract_kwargs
   gerg_plotting.modules.utilities.extract_kwargs_with_aliases
   gerg_plotting.modules.utilities.print_datetime
   gerg_plotting.modules.utilities.print_time
   gerg_plotting.modules.utilities.to_numpy_array


Module Contents
---------------

.. py:function:: calculate_pad(var, pad=0.0) -> tuple[float, float]

   Calculate padded range of values in an array.

   Parameters
   ----------
   var : array_like
       Input array to calculate padded range from
   pad : float, optional
       Amount of padding to add to both ends of the range, default is 0.0

   Returns
   -------
   tuple[float, float]
       Tuple of (min_value - pad, max_value + pad)


.. py:function:: calculate_range(var) -> list[float, float]

   Calculate the range of values in an array, ignoring NaN values.

   Parameters
   ----------
   var : array_like
       Input array to calculate range from

   Returns
   -------
   list[float, float]
       List containing [minimum, maximum] values


.. py:function:: extract_kwargs(kwargs: dict, defaults: dict)

   Extracts values from kwargs with defaults for missing keys.

   Parameters:
   -----------
   kwargs : dict
       The keyword arguments dictionary.
   defaults : dict
       A dictionary of default values for keys.

   Returns:
   --------
   dict
       A dictionary containing the extracted values.


.. py:function:: extract_kwargs_with_aliases(kwargs, defaults)

   Extracts values from kwargs, handling key aliases and defaults.

   Parameters:
   -----------
   kwargs : dict
       The keyword arguments dictionary.
   defaults : dict
       A dictionary where keys are the primary keys or tuples of aliases,
       and values are the default values.

   Returns:
   --------
   dict
       A dictionary containing the extracted values using the primary keys.


.. py:function:: print_datetime(message) -> None

   Prints a message with the current date and time in 'YYYY-MM-DD HH:MM:SS' format.

   Parameters:
       message (str): The message to include in the output.


.. py:function:: print_time(message) -> None

   Prints a message with the current time in 'HH:MM:SS' format.

   Parameters:
       message (str): The message to include in the output.


.. py:function:: to_numpy_array(values) -> numpy.ndarray

   Convert various data types to a numpy array using pandas Series as parser.

   Parameters
   ----------
   values : array_like
       Input data that can be converted to a numpy array (lists, tuples, sets, etc.)

   Returns
   -------
   np.ndarray or None
       Numpy array of the input values, or None if input is None

   Raises
   ------
   TypeError
       If input is a dictionary


