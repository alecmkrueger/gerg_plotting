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

# %%
# Method 3: Import the whole package then move to desired class or function
# -------------------------------------------------------------------------
import gerg_plotting as gp

# Initalize the data object with some sample data
data = gp.data_classes.Data(temperature=np.random.normal(28,size=1000))
hist = gp.plotting_classes.Histogram(data)  # Assign the histogram plotter to a variable

# %%
# Method 4: Import what you need from specific submodules
# --------------------------------------------------------
from gerg_plotting.plotting_classes import Histogram
from gerg_plotting.data_classes import Data

# Initalize the data object with some sample data
data = Data(temperature=np.random.normal(28,size=1000))
hist = Histogram(data)  # Assign the histogram plotter to a variable

# %%
# Method 5: Import whole submodules
# ----------------------------------
from gerg_plotting import plotting_classes, data_classes

# Initalize the data object with some sample data
data = data_classes.Data(temperature=np.random.normal(28,size=1000))
hist = plotting_classes.Histogram(data)  # Assign the histogram plotter to a variable

# %%
# Method 6: Import whole submodules with short names
# --------------------------------------------------
from gerg_plotting import plotting_classes as pc
from gerg_plotting import data_classes as dc

# Initalize the data object with some sample data
data = dc.Data(temperature=np.random.normal(28,size=1000))
hist = pc.Histogram(data)  # Assign the histogram plotter to a variable


