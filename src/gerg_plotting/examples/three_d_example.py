import mayavi.mlab
from gerg_plotting import Data,ScatterPlot3D
import pandas as pd

# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv')[::10]

df['pressure'] = df['pressure']/-1000

data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])

# Init the 3-d scatter plot
three_d = ScatterPlot3D(data)
three_d.plot('salinity',show=False)
fig = three_d.fig
three_d.plot('temperature',show=False,fig=fig)
three_d.show()
