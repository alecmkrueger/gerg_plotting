import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import matplotlib.colors
import numpy as np
from attrs import define, field, asdict
from pprint import pformat
import cmocean

from gerg_plotting.classes_data import Bathy,NonSpatialData,SpatialData,Bounds
from gerg_plotting.utils import calculate_range,get_sigma_theta

@define
class Plotter:
    instrument:SpatialData|NonSpatialData
    bounds:Bounds|None = field(default= None)

    fig:matplotlib.figure.Figure = field(default=None)
    ax:matplotlib.axes.Axes = field(default=None)

    def init_figure(self,fig=None,ax=None,three_d=False):
        if fig is None and ax is None:
            self.fig,self.ax = matplotlib.pyplot.subplots(subplot_kw={'projection':('3d' if three_d else None)})
        elif fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax
            if three_d:
                index = [idx for idx,ax in enumerate(self.fig.axes) if ax is self.ax][0]+1
                self.ax.remove()
                gs = self.ax.get_gridspec()
                self.ax = fig.add_subplot(gs.nrows,gs.ncols,index, projection='3d')

    def __getitem__(self, key:str):
        return asdict(self)[key]
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)

@define
class SurfacePlot(Plotter):
    bathy:Bathy = field(init=False)

    def init_bathy(self):
        self.bathy = Bathy(bounds=self.bounds,resolution_level=5)

    def map(self,var:str|None=None,surface_values:bool=False,fig=None,ax=None,seafloor=True):
        self.init_figure(fig,ax)
        if var is None:
            color = 'k'
            cmap = None
        else:
            color_var_values = self.instrument[var].copy()
            if surface_values:
                color_var_values[self.instrument.depth>2] = np.nan
            color = color_var_values
            cmap = self.instrument.cmaps[var]
        if self.bounds is not None:
            self.ax.set_ylim(self.bounds.lat_min,self.bounds.lat_max)
            self.ax.set_xlim(self.bounds.lon_min,self.bounds.lon_max)
        if seafloor:
            self.init_bathy()
            # Remove the white most but of the colormap
            self.bathy.cmap = cmocean.tools.crop_by_percent(self.bathy.cmap,20,'min')
            # Add land color to the colormap
            land_color = [231/255,194/255,139/255,1]
            self.bathy.cmap.set_under(land_color)
            self.ax.contourf(self.bathy.lon,self.bathy.lat,self.bathy.depth,levels=50,cmap=self.bathy.cmap,vmin=0)

        self.ax.scatter(self.instrument.lon,self.instrument.lat,c=color,cmap=cmap,s=2)
    def quiver(self):
        self.init_figure()
        raise NotImplementedError('Need to add Quiver')


@define
class VarPlot(Plotter):

    def time_series(self,var:str,fig=None,ax=None):
        self.init_figure(fig,ax)
        self.ax.scatter(self.instrument.time,self.instrument.depth,c=self.instrument[var],cmap=self.instrument.cmaps[var])
        self.ax.invert_yaxis()
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)

        self.ax.xaxis.set_major_locator(locator)
        self.ax.xaxis.set_major_formatter(formatter)
        matplotlib.pyplot.xticks(rotation=60, fontsize='small')

    def TS(self,color_var:str|None=None,cmap:matplotlib.colors.Colormap|matplotlib.colors.LinearSegmentedColormap|None=None,fig=None,ax=None):
        if not self.instrument.has_var('salinity'):
            raise ValueError('Instrument has no salinity attribute')
        if not self.instrument.has_var('temperature'):
            raise ValueError('Instrument has no temperature attribute')
        if color_var is not None:
            if not self.instrument.has_var(color_var):
                raise ValueError(f'Instrument has no {color_var} attribute')

        self.init_figure(fig,ax)
        Sg, Tg, sigma_theta = get_sigma_theta(salinity=self.instrument.salinity,temperature=self.instrument.temperature)
        cs = self.ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1,linestyles='dashed')
        matplotlib.pyplot.clabel(cs,fontsize=10,inline=True,fmt='%.1f')
        self.ax.set_xlabel('Salinity')
        self.ax.set_ylabel('Temperature (°C)')
        # self.ax.set_title(f'T-S Diagram: {glider}',fontsize=14, fontweight='bold')
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
        matplotlib.pyplot.tight_layout()
        # Plot scatter plot
        if cmap is None:
            if color_var is not None:
                cmap = self.instrument.cmaps[color_var]
            else:
                print('Using Default Color Map Viridis')
                cmap = matplotlib.pyplot.get_cmap('viridis')

        if color_var == 'density':
            from gerg_plotting.utils import get_density
            color_data = get_density(self.instrument.salinity,self.instrument.temperature)
        else:
            color_data = self.instrument[color_var]


        self.instrument.has_var(color_var)
        sc = self.ax.scatter(self.instrument.salinity,self.instrument.temperature,c=color_data,s=0.5,marker='.',cmap=cmap)
        if color_var is not None:
            cbar = matplotlib.pyplot.colorbar(sc,ax=self.ax,label=color_var)
            cbar.ax.locator_params(nbins=5)
            cbar.ax.invert_yaxis()

    def var_var(self,x:str,y:str,color_var:str|None=None,fig=None,ax=None):
        self.init_figure(fig,ax)
        if color_var is not None:
            self.ax.scatter(self.instrument[x],self.instrument[y],c=self.instrument[color_var])
        elif color_var is None:
            self.ax.scatter(self.instrument[x],self.instrument[y])

    def cross_section(self,longitude,latitude):
        raise NotImplementedError('Need to add method to plot cross sections')

@define
class Histogram(Plotter):

    def get_2d_range(self,x,y,**kwargs):
        if 'range' not in kwargs.keys():
            range = [calculate_range(self.instrument[x]),calculate_range(self.instrument[y])]
        else:
            range = kwargs['range']
            kwargs.pop('range')
        return range,kwargs

    def plot(self,var:str,fig=None,ax=None):
        self.init_figure(fig,ax)
        self.ax.hist(self.instrument[var])

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
