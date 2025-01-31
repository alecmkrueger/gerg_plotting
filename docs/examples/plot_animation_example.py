"""
Animation Example
===================================

Example of how to make an animation.


.. image:: ../examples/example_plots/animation_example.gif
    :alt: GIF of a normal distribution with increasing sample size

"""
from gerg_plotting import Data
from gerg_plotting import Histogram, Animator
import cmocean
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# sphinx_gallery_thumbnail_path = '_static/animation_example_thumb.png'

# Let's make some example data
n_points = 10000
data = Data(temperature=np.random.normal(28,size=n_points))

# Let's create a histogram function to plot the data how we would like
def make_hists(sample,color):
    '''Plot Histogram based on sample size and color'''
    data_sample = data[:10*sample+1]  # Slice data
    hist = Histogram(data_sample)  # Init histogram plotter
    hist.plot('temperature',color=color,bins=30,range=(25,31))  # Plot 1-d histogram
    hist.ax.set_ybound(upper=80)  # Set the ybounds maximum to 80 for a clearer plot
    return hist.fig

samples = np.arange(90)
cmap = plt.get_cmap('Greens')
cmap = cmocean.tools.crop_by_percent(cmap,30,which='both')
colors = [cmap((idx*2)+10) for idx in samples]

gif_filename = Path('example_plots/animation_example.gif')
Animator().animate(plotting_function=make_hists,param_dict={'sample':samples,'color':colors},fps=12,gif_filename=gif_filename)

# sphinx_gallery_start_ignore
fig = make_hists(samples[45],colors[45])
fig.savefig('../_static/animation_example_thumb.png',dpi=100)
plt.close(fig)
# sphinx_gallery_end_ignore