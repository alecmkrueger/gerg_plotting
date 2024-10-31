from gerg_plotting import Data,MapPlot,Bounds,ScatterPlot,Histogram,Variable
import pandas as pd
import cmocean

# Generate Test Data
bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
data_bounds = Bounds(lat_min = 27,lat_max = 28.5,lon_min = -96,lon_max = -89,depth_top=-1,depth_bottom=1000)
n_points = 1000
# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv')

# Let's initilize the data object
data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])

# Get the number of data points 
n_points = len(df)

# Init speed_of_sound Variable object
temp_f = Variable(data=df['speed_of_sound'],name='speed_of_sound',cmap=cmocean.cm.thermal,units='m/s',label='Speed of Sound (m/s)')
# Add the speed_of_sound Variable object to the Data object
data.add_custom_variable(temp_f)
# Test by plotting a histogram
Histogram(data).plot(var='speed_of_sound')
# Plot hovmoller 
ScatterPlot(data).hovmoller(var='speed_of_sound')
