from gerg_plotting import ScatterPlot,data_from_df
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Let's read in the example data
df = pd.read_csv('example_data/sample_tabs_data.csv')

sampling_freq = 48
segment_length = 256
highlight_freqs = [1/10, 1, 2]

for name,group in df.groupby('bin_depth'):
    data = data_from_df(group)

    fig,axes = plt.subplots(nrows=3,figsize=(10,18),layout='constrained')

    scatter = ScatterPlot(data)
    scatter.power_spectra_density(var_name='u',sampling_freq=sampling_freq,segment_length=segment_length,
                                  highlight_freqs=highlight_freqs,fig=fig,ax=axes[0])
    scatter.ax.set_title('Vector U')
    scatter.power_spectra_density(var_name='v',sampling_freq=sampling_freq,segment_length=segment_length,
                                  highlight_freqs=highlight_freqs,fig=fig,ax=axes[1])
    scatter.ax.set_title('Vector V')
    scatter.power_spectra_density(var_name='w',sampling_freq=sampling_freq,segment_length=segment_length,
                                  highlight_freqs=highlight_freqs,fig=fig,ax=axes[2])
    scatter.ax.set_title('Vector W')
    scatter.fig.suptitle(f'Auto-spectra at Bin Depth: {name} m',fontsize=24)
    plt.show()
    scatter.fig.clear()


# # Let's make an animation from this

# from gerg_plotting import Animator

# # first we need to create a function that will return the figure

# def power_spectra_plot(group):
#     data = data_from_df(group)

#     freq,psd_u,psd_v,psd_w = data.calcluate_PSD(sampling_freq=48,segment_length=256,theta_rad=np.deg2rad(55))

#     fig,axes = plt.subplots(nrows=3,figsize=(10,18),layout='constrained')

#     scatter = ScatterPlot(data)
#     scatter.power_spectra_density(freq=freq,psd=psd_u,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[0])
#     scatter.ax.set_title('Vector U')
#     scatter.power_spectra_density(freq=freq,psd=psd_v,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[1])
#     scatter.ax.set_title('Vector V')
#     scatter.power_spectra_density(freq=freq,psd=psd_w,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[2])
#     scatter.ax.set_title('Vector W')
#     scatter.fig.suptitle(f'Auto-spectra at Bin Depth: {group['bin_depth'].min()} m',fontsize=28)
#     return scatter.fig

# groups = [group for _,group in df.groupby('bin_depth')]

# Animator().animate(plotting_function=power_spectra_plot,iterable=groups,iteration_param='group',gif_filename='example_plots/power_spectra.gif',fps=1)

