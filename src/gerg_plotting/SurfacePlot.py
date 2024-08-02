from attrs import define,field
from gerg_plotting.Plotter import Plotter
from gerg_plotting.NonSpatialInstruments import Bathy
import cmocean

@define
class SurfacePlot(Plotter):
    bathy:Bathy = field(init=False)

    def init_bathy(self):
        self.bathy = Bathy(bounds=self.bounds,resolution_level=5)

    def map(self,var:str|None=None,fig=None,ax=None,seafloor=True) -> None:
        self.init_figure(fig,ax)
        if var is None:
            color = 'k'
            cmap = None
        else:
            color_var_values = self.instrument[var].copy()
            color = color_var_values
            cmap = self.get_cmap(var)
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

        sc = self.ax.scatter(self.instrument.lon,self.instrument.lat,c=color,cmap=cmap,s=3)
        self.add_colorbar(sc,var)

    def quiver(self) -> None:
        # self.init_figure()
        raise NotImplementedError('Need to add Quiver')