from gerg_plotting import MapPlot,Bounds,data_from_csv
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def map_subplots_example():
    # Define bounds
    bounds = Bounds(lat_min = 24,lat_max = 31,lon_min = -99,lon_max = -88,depth_top=-1,depth_bottom=1000)
    # Let's read in the example data
    data = data_from_csv('example_data/sample_glider_data.csv')
    data.bounds = bounds

    # Init subplots
    fig,ax = plt.subplots(figsize=(10,15),nrows=4,subplot_kw={'projection': ccrs.PlateCarree()},layout='constrained')
    # Init MapPlot object
    plotter = MapPlot(data=data,grid_spacing=3)
    # # Generate Scatter plots on one figure
    plotter.scatter(fig=fig,ax=ax[0],var='temperature',show_bathy=True,pointsize=30)
    plotter.scatter(fig=fig,ax=ax[1],var='salinity',show_bathy=True,pointsize=30)
    plotter.scatter(fig=fig,ax=ax[2],var='depth',show_bathy=True,pointsize=30)
    plotter.scatter(fig=fig,ax=ax[3],var='time',show_bathy=True,pointsize=30)
    plt.show()
    fig.savefig('example_plots/map_example.png',dpi=500,bbox_inches='tight')

if __name__ == "__main__":
    map_subplots_example()