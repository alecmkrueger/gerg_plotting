gerg_plotting.tools.tools
=========================

.. py:module:: gerg_plotting.tools.tools


Functions
---------

.. autoapisummary::

   gerg_plotting.tools.tools.create_combinations_with_underscore
   gerg_plotting.tools.tools.custom_legend_handles
   gerg_plotting.tools.tools.data_from_csv
   gerg_plotting.tools.tools.data_from_df
   gerg_plotting.tools.tools.data_from_ds
   gerg_plotting.tools.tools.data_from_netcdf
   gerg_plotting.tools.tools.interp_glider_lat_lon
   gerg_plotting.tools.tools.merge_dicts
   gerg_plotting.tools.tools.normalize_string


Module Contents
---------------

.. py:function:: create_combinations_with_underscore(strings)

   Generate pairwise combinations of strings joined by underscores.

   Parameters
   ----------
   strings : list
       List of strings to combine

   Returns
   -------
   list
       List of combined strings including original strings


.. py:function:: custom_legend_handles(labels: list[str], colors, hatches=None, color_hatch_not_background: bool = False)

   Create custom legend handles with specified colors and patterns.

   Parameters
   ----------
   labels : list[str]
       List of legend labels
   colors : list
       List of colors for patches
   hatches : list, optional
       List of hatch patterns
   color_hatch_not_background : bool, optional
       Whether to color hatch instead of background

   Returns
   -------
   list
       List of matplotlib patch objects for legend


.. py:function:: data_from_csv(filename: str, mapped_variables: dict | None = None, **kwargs)

   Create Data object from CSV file.

   Parameters
   ----------
   filename : str
       Path to CSV file
   mapped_variables : dict, optional
       Custom variable mapping
   ``**kwargs``
       Additional arguments for Data initialization

   Returns
   -------
   Data
       Initialized Data object


.. py:function:: data_from_df(df: pandas.DataFrame, mapped_variables: dict | None = None, **kwargs)

   Create Data object from DataFrame.

   Parameters
   ----------
   df : pandas.DataFrame
       Source DataFrame
   mapped_variables : dict, optional
       Custom variable mapping
   ``**kwargs`` : dict
       Additional arguments for Data initialization

   Returns
   -------
   Data
       Initialized Data object


.. py:function:: data_from_ds(ds: xarray.Dataset, mapped_variables: dict | None = None, **kwargs)

   Create Data object from xarray Dataset.

   Parameters
   ----------
   ds : xarray.Dataset
       Input dataset to convert
   mapped_variables : dict or None, optional
       Dictionary mapping variable names to dataset variables
   ``**kwargs``
       Additional keyword arguments passed to Data constructor

   Returns
   -------
   Data
       New Data object containing the dataset variables


.. py:function:: data_from_netcdf(filename: str, mapped_variables: dict | None = None, interp_glider: bool = False, **kwargs)

   Create Data object from NetCDF file.

   Parameters
   ----------
   filename : str
       Path to NetCDF file
   mapped_variables : dict or None, optional
       Dictionary mapping variable names to dataset variables  
   interp_glider : bool, optional
       Whether to interpolate glider lat/lon positions
   ``**kwargs``
       Additional keyword arguments passed to Data constructor

   Returns
   -------
   Data
       New Data object containing the NetCDF variables


.. py:function:: interp_glider_lat_lon(ds: xarray.Dataset) -> xarray.Dataset

   Interpolate glider latitude and longitude data.

   Parameters
   ----------
   ds : xarray.Dataset
       Dataset containing glider data

   Returns
   -------
   xarray.Dataset
       Dataset with interpolated lat/lon coordinates


.. py:function:: merge_dicts(*dict_args)

   Merge multiple dictionaries with later dictionaries taking precedence.

   Parameters
   ----------
   ``*dict_args`` : dict
       Variable number of dictionaries to merge

   Returns
   -------
   dict
       New dictionary containing merged key-value pairs


.. py:function:: normalize_string(input_string: str) -> str

   Normalize string by converting to lowercase and standardizing special characters.

   Parameters
   ----------
   input_string : str
       String to normalize

   Returns
   -------
   str
       Normalized string with special characters replaced by underscores

   Raises
   ------
   ValueError
       If input is not a string


