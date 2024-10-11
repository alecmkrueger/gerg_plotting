import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import numpy as np
from attrs import define, field


from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.utils import get_sigma_theta,get_density
from gerg_plotting.data_classes.NonSpatialInstruments import Variable

@define
class VarPlot(Plotter):
    markersize:int|float = field(default=10)

    def depth_time_series(self,var:str,fig=None,ax=None) -> None:
        self.init_figure(fig,ax)
        sc = self.ax.scatter(self.instrument.time.data,self.instrument.depth.data,
                        c=self.instrument[var].data,cmap=self.instrument.cmaps[var],
                        s=self.markersize)
        self.ax.invert_yaxis()
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)

        self.ax.xaxis.set_major_locator(locator)
        self.ax.xaxis.set_major_formatter(formatter)
        matplotlib.pyplot.xticks(rotation=60, fontsize='small')
        self.add_colorbar(sc,var=var)

    def check_ts(self,color_var:str=None) -> None:
        if not self.instrument._has_var('salinity'):
            raise ValueError('Instrument has no salinity attribute')
        if not self.instrument._has_var('temperature'):
            raise ValueError('Instrument has no temperature attribute')
        if color_var is not None:
            if not self.instrument._has_var(color_var):
                raise ValueError(f'Instrument has no {color_var} attribute')
 
    def format_ts(self,fig,ax,contours:bool=True) -> None:
        self.check_ts()
        self.init_figure(fig,ax)
        if contours:
            Sg, Tg, sigma_theta = get_sigma_theta(salinity=self.instrument['salinity'].data,temperature=self.instrument['temperature'].data)
            cs = self.ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1,linestyles='dashed')
            matplotlib.pyplot.clabel(cs,fontsize=10,inline=True,fmt='%.1f')
        self.ax.set_xlabel('Salinity')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.set_title(f'T-S Diagram',fontsize=14, fontweight='bold')
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=8))

    def TS(self,fig=None,ax=None,contours:bool=True) -> None:
        '''Temperature vs Salinity plot. The contours can take a long time to calculate, consider turning them off if you do not need them'''
        self.format_ts(fig,ax,contours)
        self.ax.scatter(self.instrument['salinity'].data,self.instrument['temperature'].data,s=self.markersize,marker='.')

    def get_density_color_data(self,color_var:str) -> np.ndarray:
        # If there is no density data in the instrument
        if color_var == 'density':
            if not isinstance(self.instrument['density'],Variable):  # if the attribute 'density' is not a Variable object, and thus not passed by the user            
                color_data = get_density(self.instrument['salinity'].data,self.instrument['temperature'].data)  # Calculate the density
            else:
                color_data = self.instrument[color_var].data
        else:
            color_data = self.instrument[color_var].data
        return color_data

    def TS_with_color_var(self,color_var:str,fig=None,ax=None,contours:bool=True) -> None:
        '''Temperature vs Salinity plot with a color variable. The contours can take a long time to calculate, consider turning them off if you do not need them'''
        self.format_ts(fig,ax,contours)
        cmap = self.get_cmap(color_var)
        color_data = self.get_density_color_data(color_var)

        sc = self.ax.scatter(self.instrument['salinity'].data,self.instrument['temperature'].data,c=color_data,s=self.markersize,marker='.',cmap=cmap)
        self.add_colorbar(sc,color_var)

    def var_var(self,x:str,y:str,color_var:str|None=None,fig=None,ax=None) -> None:
        self.init_figure(fig,ax)
        if color_var is not None:
            self.ax.scatter(self.instrument[x].data,self.instrument[y].data,c=self.instrument[color_var].data)
        elif color_var is None:
            self.ax.scatter(self.instrument[x].data,self.instrument[y].data)

    def cross_section(self,longitude,latitude) -> None:
        raise NotImplementedError('Need to add method to plot cross sections')