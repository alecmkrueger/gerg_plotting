from attrs import define
import numpy as np
import matplotlib.pyplot as plt
from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.utils import calculate_range

@define
class Histogram(Plotter):
    def get_2d_range(self,x,y,**kwargs):
        # If the range was not passed then caclulate it and return it
        if 'range' not in kwargs.keys():
            range = [calculate_range(self.instrument[x].data),calculate_range(self.instrument[y].data)]
        # Check if range was passed with **kwargs and if so, remove it from the kwargs and return it
        else:
            range = kwargs['range']
            kwargs.pop('range')
        # Return both the range and the kwargs with the range kwarg removed
        return range,kwargs

    def plot(self,var:str,fig=None,ax=None,bins=30):
        self.init_figure(fig,ax)
        self.ax.hist(self.instrument[var].data,bins=bins)
        self.ax.set_ylabel('Count')
        self.ax.set_xlabel(f'{var} ({self.instrument.units[var]})')

    def plot2d(self,x:str,y:str,fig=None,ax=None,**kwargs):
        self.init_figure(fig,ax)
        range,kwargs = self.get_2d_range(x,y,**kwargs)
        hist = self.ax.hist2d(self.instrument[x].data,self.instrument[y].data,range=range,**kwargs)
        self.ax.set_xlabel(self.instrument[x].label)
        self.ax.set_ylabel(self.instrument[y].label)
        cbar = plt.colorbar(hist[3],ax=self.ax,label='Count',orientation='horizontal')
        # cbar.ax.tick_params(rotation=90)


    def plot3d(self,x:str,y:str,fig=None,ax=None,**kwargs):
        from matplotlib import cm
        self.init_figure(fig,ax,three_d=True)
        range,kwargs = self.get_2d_range(x,y,**kwargs)
        h,xedges,yedges = np.histogram2d(self.instrument[x].data,self.instrument[y].data,range=range,**kwargs)
        X,Y = np.meshgrid(xedges[1:],yedges[1:])
        self.ax.plot_surface(X,Y,h, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        self.ax.zaxis.set_rotate_label(False) 
        self.ax.set_zlabel('Count', rotation = 90)
        self.ax.set_xlabel(self.instrument[x].label)
        self.ax.set_ylabel(self.instrument[y].label)
        self.ax.view_init(elev=30, azim=45)