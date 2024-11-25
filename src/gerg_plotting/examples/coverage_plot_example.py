from gerg_plotting.plotting_classes.CoveragePlot import CoveragePlot

import matplotlib.pyplot as plt
import numpy as np


def coverage_plot_example():
    # Define the cmap we will use
    cmap = 'tab20'
    # Define the x and y labels
    x_labels = ['Seconds','Minutes','Hours','Days','Weeks','Months','Years','Decades']
    y_labels = ['Surface','10-100\nMeters','100-500\nMeters','Below 500\nMeters','Benthos']
    # Init the coverage plotter
    plotter = CoveragePlot(x_labels=x_labels,y_labels=y_labels,
                        colormap=cmap,figsize=(12,6),coverage_fontsize=10.5,
                        grid_linestyle='--',grid_linewidth=0.9)
    # Init plot with the x and y labels and the axes bounds limit, must do before adding coverages
    plotter.set_up_plot(horizontal_padding=0.25,vertical_padding=0.75)
    # All Depths
    plotter.add_coverage(x_range=[7,8],y_range=[-0.45,4.2],label='Climate\nScience')
    plotter.add_coverage(x_range=[5,7],y_range=[-0.45,4.2],label='Fisheries')
    # Surface
    plotter.add_coverage(x_range=[3,8],y_range=[-0.15,-0.15],label='Oil and Gas')
    plotter.add_coverage(x_range=[2,4],y_range=[-0.45,-0.45],label='Search and Rescue')
    plotter.add_coverage(x_range=[3,8],y_range=[0.15,0.15],label='Wind and Algal Blooms')
    # 10-100m
    plotter.add_coverage(x_range=[2,5],y_range=[0.85,0.85],label='Hurricane Forcasting')
    plotter.add_coverage(x_range=[3,7],y_range=[1.15,1.15],label='Hypoxia')
    # Below 500m
    plotter.add_coverage(x_range=[3,8],y_range=[2.85,2.85],label='Oil and Gas',fc=plotter.colormap(2))

    plotter.ax.tick_params(axis='x', labeltop=True, labelbottom=False)

    plotter.fig.tight_layout()

    plotter.fig.savefig('example_plots/coverage_plot_example.png',dpi=600)


if __name__ == "__main__":
    coverage_plot_example()
