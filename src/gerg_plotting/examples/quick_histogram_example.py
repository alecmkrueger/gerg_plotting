from gerg_plotting import Data,Histogram
import numpy as np

data = Data(temperature=np.random.normal(28,size=1000))

Histogram(data).plot(var='temperature')
