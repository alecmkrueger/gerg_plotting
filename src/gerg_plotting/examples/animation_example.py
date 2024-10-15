from gerg_plotting import Data,Histogram,Animator,Variable
import numpy as np

n_points = 10000

data = Data(temperature=np.random.normal(28,size=n_points),salinity=np.random.normal(35.25,scale=0.25,size=n_points))
pH = Variable(data=np.random.normal(7.7,scale=0.25,size=n_points),name='pH')
data.add_custom_variable(pH)

def make_hists(sample,data=data):
    data_sample = data[:10*sample+1]
    hist = Histogram(data_sample)
    hist.plot('temperature')
    return hist.fig

Animator().animate(plotting_function=make_hists,iterable=range(90),iteration_param='sample',gif_filename='hist.gif')
