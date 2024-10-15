from gerg_plotting import Data,Variable,Bounds
from gerg_plotting.utils import generate_random_point

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import cmocean

# We will create a few Data objects below using various methods

# Let's make some example data
n_points = 1000
data_bounds = Bounds(lat_min = 27,lat_max = 28.5,lon_min = -96,lon_max = -89,depth_top=-1,depth_bottom=1000)
lats,lons = np.transpose([generate_random_point(lat_min=data_bounds.lat_min,
                                                lat_max=data_bounds.lat_max,
                                                lon_min=data_bounds.lon_min,
                                                lon_max=data_bounds.lon_max) for _ in range(n_points)])
depth = np.random.uniform(low=-200,high=0,size=n_points)
time = pd.Series(pd.date_range(start='10-01-2024',end='10-10-2024',periods=n_points)).astype('datetime64[s]')
salinity = np.random.uniform(low=28,high=32,size=n_points)
temperature = np.random.uniform(low=5,high=28,size=n_points)
density = np.random.uniform(1024,1031,size=n_points)

# Let's also create a dataframe, example for if your data was read in from a csv file using pandas
df = pd.DataFrame([lats,lons,depth,time,salinity,temperature,density]).T
df.columns = ['lat','lon','depth','time','salinity','temperature','density']  # Add column names


# Method 1: Using Iterables

# Here is the initialization of the Data object used for plotting using pandas.Series objects as the inputs
# To use this method you must use one of the default variables, there is another method for adding non-default/custom variables
data = Data(lat=df['lat'],lon=df['lon'],depth=df['depth'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])
# Here is an example using numpy arrays:
data = Data(lat=lats,lon=lons,depth=depth,time=time,salinity=salinity,temperature=temperature,density=density)



# Method 2: Using Variable Objects

# There is a bit more to do before we can initialize the Data object
# This way we can be clear with our variable creation

# Let's initialize the Variable objects
lat_var = Variable(data = lats,name='lat', cmap=cmocean.cm.haline, units='°N', vmin=None, vmax=None)
lon_var = Variable(data = lons,name='lon', cmap=cmocean.cm.thermal, units='°W', vmin=None, vmax=None)
depth_var = Variable(data = depth,name='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
time_var = Variable(data = time,name='time', cmap=cmocean.cm.thermal, units=None, vmin=None, vmax=None)

temperature_var = Variable(data = temperature,name='temperature', cmap=cmocean.cm.thermal, units='°C', vmin=-10, vmax=40)
salinity_var = Variable(data = salinity,name='salinity', cmap=cmocean.cm.haline, units=None, vmin=28, vmax=40)
density_var = Variable(data = density,name='density', cmap=cmocean.cm.dense, units="kg/m\u00B3", vmin=1020, vmax=1035)

# Now that we have our Variables we can initialize the Data object just like before
data = Data(lat=lat_var,lon=lon_var,depth=depth_var,time=time_var,
            temperature=temperature_var,salinity=salinity_var,density=density_var)


# You can see that there are a few attributes in the Variable object initialization
# To change any attribute of any variable just reassign after the init like this:
data['lat'].vmin = 27
data['depth'].units = 'km'
# or like this:
data.lat.vmin = 27
data.depth.units = 'km'
# You can even reassign an entire variable like this:
data['lat'] = Variable(data = lats, name='lat', cmap=cmocean.cm.haline, units='°N', vmin=27, vmax=28.5)


# Assigning a variable that is a non-default/custom variable is very similar:
# First we must initialize the variable
pH = np.random.uniform(7.7,8.1,n_points)
pH_var = Variable(data = pH, name = 'pH',cmap=cmocean.cm.thermal, units=None, vmin=7.7,vmax=8.1,label='pH')
# Then we can assign it
data.add_custom_variable(pH_var)
# We can also do this in one line:
data.add_custom_variable(Variable(data = np.random.uniform(7.7,8.1,n_points), name = 'pH', cmap=cmocean.cm.thermal, units=None, vmin=7.7, vmax=8.1, label='pH'))

