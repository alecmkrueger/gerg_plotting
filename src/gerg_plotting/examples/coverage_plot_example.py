from gerg_plotting.plotting_classes.CoveragePlot import CoveragePlot

import matplotlib.pyplot as plt
import numpy as np


# palette = ['#275C62', '#298880', '#5AA786','#8AB17D','#E9C46A','#F4A261','#E76F51']
# palette = ['#298880', '#8AB17D', '#BABB74','#E9C46A','#F4A261','#EE8959','#E76F51']

# cmap = matplotlib.colors.ListedColormap(palette)
# n_colors = len(palette)

def coverage_plot_example():
    cmap = 'tab20'
    n_colors = 20

    x_labels = ['Seconds','Minutes','Hours','Days','Weeks','Month','Years','Decades']
    y_labels = ['Surface','10-100\nmeters','100-500\nmeters','Below 500\nmeters','Benthos']


    fig,ax = plt.subplots(figsize=(11,7))

    plotter = CoveragePlot(x_labels=x_labels,y_labels=y_labels,
                        colormap=cmap,n_colors=n_colors)
    # Init plot with the x and y labels and the axes bounds limit
    plotter.set_up_plot(fig=fig,ax=ax,padding=0.25)
    # Add grid
    plotter.add_hlines(np.arange(-0.5,5.5,1),linewidth=1.25,ls='--',color='gray')
    plotter.add_vlines(np.arange(0,9,1),linewidth=1.25,ls='--',color='gray')
    # All Depths
    plotter.add_coverage(x_range=[7,8],y_range=[-0.45,4.2],label='Climate\nScience')
    plotter.add_coverage(x_range=[5,6],y_range=[-0.45,4.2],label='Fisheries')
    # Surface
    plotter.add_coverage(x_range=[3,7],y_range=[-0.15,-0.15],label='Oil and Gas')
    plotter.add_coverage(x_range=[2,3],y_range=[-0.45,-0.45],label='SAR')
    plotter.add_coverage(x_range=[3,7],y_range=[0.15,0.15],label='Wind and Algal Blooms')
    # 10-100m
    plotter.add_coverage(x_range=[2,4],y_range=[0.85,0.85],label='Hurricane Forcasting')
    plotter.add_coverage(x_range=[3,6],y_range=[1.15,1.15],label='Hypoxia')
    # Below 500m
    plotter.add_coverage(x_range=[3,7],y_range=[3,3],label='Oil and Gas',fc=plotter.colormap(2))

    plotter.save('example_plots/coverage_plot_example.png')


if __name__ == "__main__":
    coverage_plot_example()
