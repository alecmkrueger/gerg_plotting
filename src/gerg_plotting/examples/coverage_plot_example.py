from gerg_plotting.plotting_classes.CoveragePlot import CoveragePlot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cmocean
from matplotlib.ticker import FixedLocator


def coverage_plot_example():
    df = pd.read_csv('example_data/stakeholder.csv')
    df = df[5:].reset_index(drop=True)
    df = df[df['index']!='TIME'].reset_index(drop=True)
    df = df.T
    df.columns = df.loc['index']
    df = df.drop('index')

    def point_sum(df:pd.DataFrame,column1:str,column2:str):
        xx = df[column1]
        yy = df[column2]
        total = 0
        for x,y in zip(xx,yy):
            if x ==1 and y==1:
                total +=1
        return total


    depths = ['Surface','Midwater','Benthic']
    times = ['Seconds', 'Minutes', 'Hours', 'Days','Weeks', 'Months', 'Years', 'Decades']

    df_summary = pd.DataFrame(np.zeros((len(depths),len(times))))

    for depth_idx,depth in enumerate(depths):
        for time_idx,time in enumerate(times):
            df_summary.at[depth_idx,time_idx] = point_sum(df,depth,time)

    # Prepare data for 3D plotting
    x, y = np.meshgrid(df_summary.columns, df_summary.index)
    x = x.ravel()  # Flatten the mesh grid for plotting
    y = y.ravel()
    z = np.zeros_like(x)  # Base of the bars
    dx = dy = 0.8  # Width and depth of the bars
    dz = df_summary.values.ravel()  # Heights (flattened DataFrame values)
    colors = plt.get_cmap("viridis")(dz)

    # Plot the 3D histogram
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    cmap=cmocean.cm.thermal(plt.Normalize(0,max(dz))(dz))
    ax.bar3d(x, y, z, dx, dy, dz, shade=True, color=cmap)
    ax.set_zlabel('Count')
    ax.set_title('3D Histogram')

    def add_labels(axis,labels):
        if axis.lower() == 'x':
            major_locator = ax.xaxis.set_major_locator
            label_setter = ax.set_xticklabels
            tick_positions = np.arange(0.5,len(labels)+0.5)  # Tick positions
            
        elif axis.lower() == 'y':
            major_locator = ax.yaxis.set_major_locator
            label_setter = ax.set_yticklabels  
            tick_positions = np.arange(0,len(labels))  # Tick positions     

        major_locator(FixedLocator(tick_positions))
        label_setter(labels)

    add_labels('y',depths)
    add_labels('x',times)
    ax.view_init(30, 70)
    plt.show()



# surface_seconds = 
# def coverage_plot_example():
#     cmap = 'tab20'
#     # Define the x and y labels
#     x_labels = ['Seconds','Minutes','Hours','Days','Weeks','Months','Years','Decades']
#     y_labels = ['Surface','10-100\nMeters','100-500\nMeters','Below 500\nMeters','Benthos']
#     # Init the coverage plotter
#     plotter = CoveragePlot(x_labels=x_labels,y_labels=y_labels,colormap=cmap,
#                            figsize=(12,6),coverage_fontsize=10.5,coverage_linewidth=3,
#                            grid_linestyle='--',grid_linewidth=0.9,coverage_alpha=0.5,coverage_min_rectangle_height=0.25)
#     # All Depths
#     plotter.add_coverage(x_range=['Seconds','Decades'],y_range=['Surface','Benthos'],label='Academic')
#     plotter.add_coverage(x_range=['Days','Months'],y_range=['Surface','Benthos'],label='Consultants')
#     plotter.add_coverage(x_range=['Days','Years'],y_range=[-0.25,'Benthos'],label='Regulatory')
#     plotter.add_coverage(x_range=['Days','Decades'],y_range=['Surface','Benthos'],label='Oil and Gas')
#     plotter.add_coverage(x_range=['Months','Years'],y_range=['Surface','Benthos'],label='Fisheries')
#     plotter.add_coverage(x_range='Decades',y_range=['Surface','Benthos'],label='Climate\nScience')

#     # Surface
#     plotter.add_coverage(x_range=['Hours','Days'],y_range=[-0.5,-0.5],label='Search and Rescue')
#     plotter.add_coverage(x_range=['Days','Decades'],y_range=[-0.5,-0.5],label='Wind and Algal Blooms')
#     # 10-100m
#     plotter.add_coverage(x_range=['Hours','Weeks'],y_range=[0.5,0.5],label='Hurricane Forcasting')
#     plotter.add_coverage(x_range=['Days','Years'],y_range=[0.5,0.5],label='Hypoxia')

#     plotter.plot()
#     # plotter.fig.savefig('example_plots/coverage_plot_example.png',dpi=600)


if __name__ == "__main__":
    coverage_plot_example()
