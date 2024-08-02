from attrs import define
from gerg_plotting.Plotter import Plotter
from gerg_plotting.utils import calculate_range

@define
class Histogram(Plotter):

    def get_2d_range(self,x,y,**kwargs):
        # If the range was not passed then caclulate it and return it
        if 'range' not in kwargs.keys():
            range = [calculate_range(self.instrument[x]),calculate_range(self.instrument[y])]
        # Check if range was passed with **kwargs and if so, remove it from the kwargs and return it
        else:
            range = kwargs['range']
            kwargs.pop('range')
        # Return both the range and the kwargs with the range kwarg removed
        return range,kwargs

    def plot(self,var:str,fig=None,ax=None,bins=30):
        self.init_figure(fig,ax)
        self.ax.hist(self.instrument[var],bins=bins)

    def plot2d(self,x:str,y:str,fig=None,ax=None,**kwargs):
        self.init_figure(fig,ax)
        range,kwargs = self.get_2d_range(x,y,**kwargs)
        self.ax.hist2d(self.instrument[x],self.instrument[y],range=range,**kwargs)

    def plot3d(self,x:str,y:str,fig=None,ax=None,**kwargs):
        from matplotlib import cm
        self.init_figure(fig,ax,three_d=True)
        range,kwargs = self.get_2d_range(x,y,**kwargs)
        h,xedges,yedges = np.histogram2d(self.instrument[x],self.instrument[y],range=range,**kwargs)
        X,Y = np.meshgrid(xedges[1:],yedges[1:])
        self.ax.plot_surface(X,Y,h, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)