"""
Custom Variable Example
===================================

How to add a custom variable to a Data object and plot a histogram of it.

"""
from gerg_plotting import Data,Variable,Histogram
import numpy as np

# Init Data object
data = Data()
# Init pH Variable object
pH = Variable(values=np.random.normal(7.7,scale=0.25,size=1000),name='pH')
# Add the pH Variable object to the Data object
data.add_custom_variable(pH)
# Test by plotting a histogram
hist = Histogram(data)
hist.plot('pH')
hist.save('example_plots/custom_variable_example.png')
