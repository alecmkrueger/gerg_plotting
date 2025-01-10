from attrs import define,field,asdict
from pprint import pformat
from typing import Iterable
import cmocean
import copy
import matplotlib.dates as mdates
import numpy as np


from gerg_plotting.data_classes.Variable import Variable
from gerg_plotting.data_classes.Bounds import Bounds
from gerg_plotting.modules.utilities import calculate_pad


@define(slots=False)
class SpatialInstrument:
    """
    A class representing spatial instrument data with geographic coordinates and measurements.

    This class handles spatial data with latitude, longitude, depth, and time dimensions,
    along with custom variables. It provides methods for data access, manipulation, and bounds detection.

    Parameters
    ----------
    lat : Iterable | Variable | None
        Latitude values or Variable object containing latitude data
    lon : Iterable | Variable | None
        Longitude values or Variable object containing longitude data
    depth : Iterable | Variable | None
        Depth values or Variable object containing depth data
    time : Iterable | Variable | None
        Time values or Variable object containing temporal data
    bounds : Bounds, optional
        Geographic and depth bounds for the dataset
    custom_variables : dict
        Dictionary to store additional custom variables

    Methods
    -------
    copy()
        Creates a deep copy of the instrument object
    slice_var(var: str, slice: slice)
        Slices data for a specific variable
    get_vars()
        Returns list of all available variables
    check_for_vars(vars: list)
        Verifies presence of required variables
    detect_bounds(bounds_padding=0)
        Automatically detects data bounds with optional padding
    add_custom_variable(variable: Variable, exist_ok: bool)
        Adds a new custom variable to the instrument
    remove_custom_variable(variable_name)
        Removes a custom variable from the instrument
    """
    # Dims
    lat: Iterable|Variable|None = field(default=None)
    lon: Iterable|Variable|None = field(default=None)
    depth: Iterable|Variable|None = field(default=None)
    time: Iterable|Variable|None = field(default=None)

    # Bounds
    bounds:Bounds = field(default=None)
    
    # Custom variables dictionary to hold dynamically added variables
    custom_variables: dict = field(factory=dict)


    def __attrs_post_init__(self) -> None:
        """Initializes the instrument with standard dimensions and formats datetime data."""
        self._init_dims()
        self._format_datetime()


    def copy(self):
        """Creates a deep copy of the instrument object."""
        self_copy = copy.deepcopy(self)
        return self_copy
    

    def slice_var(self,var:str,slice:slice) -> np.ndarray:
        """Slices data for a specific variable."""
        return self[var].data[slice]


    def _has_var(self, key) -> bool:
        """Checks if a variable exists in the instrument."""
        return key in asdict(self).keys() or key in self.custom_variables
    

    def get_vars(self) -> list:
        """Gets a list of all available variables."""
        vars = list(asdict(self).keys()) + list(self.custom_variables.keys())
        vars = [var for var in vars if var!='custom_variables']
        return vars


    def __getitem__(self, key) -> Variable:
        """Allows accessing standard and custom variables via indexing."""
        if isinstance(key,slice):
            self_copy = self.copy()
            for var_name in self.get_vars():
                if isinstance(self_copy[var_name],Variable):
                    self_copy[var_name].data = self.slice_var(var=var_name,slice=key)
            return self_copy
        elif self._has_var(key):
            return getattr(self, key, self.custom_variables.get(key))
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")    


    def __setitem__(self, key, value) -> None:
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            if key in asdict(self):
                setattr(self, key, value)
            else:
                self.custom_variables[key] = value
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")


    def __repr__(self) -> None:
        '''Pretty printing'''
        return pformat(asdict(self),width=1)
    

    def _init_dims(self):
        """Initialize standard dimensions (lat, lon, depth, time) as Variable objects."""
        self._init_variable(var='lat', cmap=cmocean.cm.haline, units='°N', vmin=None, vmax=None)
        self._init_variable(var='lon', cmap=cmocean.cm.thermal, units='°E', vmin=None, vmax=None)
        self._init_variable(var='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
        self._init_variable(var='time', cmap=cmocean.cm.thermal, units=None, vmin=None, vmax=None)

    def _format_datetime(self) -> None:
        """Format datetime data as numpy datetime64 objects."""
        if self.time is not None:
            if self.time.data is not None:
                self.time.data = self.time.data.astype('datetime64[ns]')

    def _init_variable(self, var: str, cmap, units, vmin, vmax) -> None:
        """
        Initialize a standard variable as a Variable object.

        Parameters
        ----------
        var : str
            Name of the variable to initialize
        cmap : matplotlib.colors.Colormap
            Colormap for variable visualization
        units : str
            Units of the variable
        vmin : float | None
            Minimum value for visualization
        vmax : float | None
            Maximum value for visualization
        """        
        if self._has_var(var):
            if not isinstance(self[var],Variable):
                if self[var] is not None:    
                    self[var] = Variable(
                        data=self[var],
                        name=var,
                        cmap=cmap,
                        units=units,
                        vmin=vmin,
                        vmax=vmax
                    )
        else:
            raise ValueError(f'{var} does not exist, try using the add_custom_variable method')
        


    def check_for_vars(self,vars:list) -> bool:
        """
        Verify that all required variables exist in the dataset.

        Parameters
        ----------
        vars : list
            List of variable names to check

        Returns
        -------
        bool
            True if all variables exist

        Raises
        ------
        ValueError
            If any required variables are missing
        """
        vars = [var for var in vars if var is not None]
        vars = [var for var in vars if self[var] is None]
        if vars:
            raise ValueError(
                f"The following required variables are missing: {', '.join(vars)}. "
                "Please ensure the Data object includes data for all listed variables."
            )
        return True


    def date2num(self) -> list:
        """Converts time data to numerical values."""
        if self.time is not None:
            if self.time.data is not None:
                return list(mdates.date2num(self.time.data))
        else: raise ValueError('time variable not present')


    def detect_bounds(self,bounds_padding=0) -> Bounds:
        '''
        Detect the geographic bounds of the data, applying padding if specified.

        An intentional effect of this function:
            will only calculate the bounds when self.bounds is None,
            so that it does not overwrite the user's custom bounds,
            this will also ensure that the bounds is not repeatedly calculated unless desired,
            can recalculate self.bounds using a new bounds_padding value if self.bounds is set to None

        The depth bounds are not affected by the bounds padding, therfore the max and min values of the depth data are used

        Parameters
        ----------
        bounds_padding : float, optional
            Padding to add to the detected bounds, by default 0

        Returns
        -------
        Bounds
            Object containing the detected geographic and depth bounds
        """

        '''
        # If the user did not pass bounds
        if self.bounds is None:
            # Detect and calculate the lat bounds with padding
            if self.lat is not None:
                lat_min, lat_max = calculate_pad(self.lat.data, pad=bounds_padding)
            else:
                lat_min, lat_max = None, None
            # Detect and calculate the lon bounds with padding
            if self.lon is not None:
                lon_min, lon_max = calculate_pad(self.lon.data, pad=bounds_padding)
            else:
                lon_min, lon_max = None, None
            
            # depth_bottom: positive depth example: 1000
            # depth_top:positive depth example for surface: 0
            
            if self.depth is not None:
                depth_top, depth_bottom = calculate_pad(self.depth.data)
            else:
                depth_top, depth_bottom = None,None
                
            # Set the bounds
            self.bounds = Bounds(
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                depth_bottom=depth_bottom,
                depth_top=depth_top
            )

        return self.bounds


    def add_custom_variable(self, variable: Variable, exist_ok:bool=False) -> None:
        """
        Adds a custom Variable object and makes it accessible via both dot and dict syntax.
        If exist_ok is True then if the variable already exists it will be replaced
        """
        if not isinstance(variable, Variable):
            raise TypeError(f"The provided object is not an instance of the Variable class.")
        
        if hasattr(self, variable.name) and not exist_ok:
            raise AttributeError(f"The variable '{variable.name}' already exists.")
        else:
            # Add to custom_variables and dynamically create the attribute
            self.custom_variables[variable.name] = variable
            setattr(self, variable.name, variable)


    def remove_custom_variable(self,variable_name) -> None:
        '''Removes a custom variable'''
        delattr(self,variable_name)

