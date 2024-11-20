from gerg_plotting import ScatterPlot,Histogram,Variable,data_from_df,ScatterPlot3D
from gerg_plotting.modules.plotting import get_turner_cmap
import pandas as pd


def custom_variable_example():
    # Let's read in the example data
    df = pd.read_csv('example_data/sample_glider_data_test.csv')

    # Let's initilize the data object
    data = data_from_df(df)

    cmap = get_turner_cmap()

    # Init Turner_Rsubrho Variable object
    Turner_Rsubrho = Variable(data=df['Turner_Rsubrho'],name='Turner_Rsubrho',cmap=cmap,units='m/s',vmin=-90,vmax=90)
    # Add the Turner_Rsubrho Variable object to the Data object
    data.add_custom_variable(Turner_Rsubrho)
    # Test by plotting a histogram
    Histogram(data).plot(var='Turner_Rsubrho')
    # Plot hovmoller 
    ScatterPlot(data).hovmoller(var='Turner_Rsubrho')
    # Plot 3d map
    ScatterPlot3D(data).map(var='Turner_Rsubrho',vertical_scalar=-1000)


if __name__ == "__main__":
    custom_variable_example()