"""
Simple Custom Variable Example
===================================

Example description

.. image:: ../examples/example_plots/simple_custom_variable_example.png
    :alt: Pre-generated image for this example

"""
from gerg_plotting.data_classes import Data,Variable
from gerg_plotting.plotting_classes import Histogram
import numpy as np

# Init Data object
data = Data()
# Init pH Variable object
pH = Variable(data=np.random.normal(7.7,scale=0.25,size=1000),name='pH')
# Add the pH Variable object to the Data object
data.add_custom_variable(pH)
# Test by plotting a histogram
hist = Histogram(data)
hist.plot('pH')
hist.save('example_plots/simple_custom_variable_example.png')
