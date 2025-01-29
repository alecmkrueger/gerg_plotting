"""
Histogram Example
===================================

Example description

"""
from gerg_plotting.plotting_classes import Histogram
from gerg_plotting.data_classes import Data
import numpy as np

# Initalize the data object with some sample data
data = Data(temperature=np.random.normal(28,size=1000))

hist = Histogram(data)  # Assign the histogram plotter to a variable
hist.plot(var='temperature')

hist.save('example_plots/histogram_example.png')
