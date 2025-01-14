from gerg_plotting.plotting_classes import ScatterPlot
from gerg_plotting.tools import data_from_csv


def simple_scatter_plot_example():
    """
    Simple Scatter Plot Example
    -----------
    Source Code
    ~~~~~~~~~~
    .. literalinclude:: ../../../src\examples\simple_scatter_plot_example.py
       :language: python

    Output
    ~~~~~~
    .. image:: ../../../src\examples\simple_scatter_plot_example.png
       :width: 600
    
    """
    # Let's read in the example data
    data = data_from_csv('example_data/sample_glider_data.csv')

    scatter = ScatterPlot(data)
    scatter.scatter('time','temperature')
    scatter.save('example_plots/simple_scatter_plot_example.png')

if __name__ == "__main__":
    simple_scatter_plot_example()