from gerg_plotting import Data,Scatter3D
import pandas as pd

# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv')[::10]

df['pressure'] = df['pressure']/-1000

data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])

Scatter3D(data).plot()
