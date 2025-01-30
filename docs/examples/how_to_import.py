"""
How to import gerg_plotting
==================================================

This example shows some of the different ways to import the gerg_plotting package.

"""
#%%
# Method 1: Import just what you need
# ------------------------------------

# sphinx_gallery_start_ignore
import numpy as np
# sphinx_gallery_end_ignore
from gerg_plotting import Data, Histogram
# Initalize the data object with some sample data
data = Data(temperature=np.random.normal(28,size=1000))
hist = Histogram(data)  # Assign the histogram plotter to a variable

# %%
# Method 2: Import the whole package
# ------------------------------------
import gerg_plotting as gp

# Initalize the data object with some sample data
data = gp.Data(temperature=np.random.normal(28,size=1000))
hist = gp.Histogram(data)  # Assign the histogram plotter to a variable



