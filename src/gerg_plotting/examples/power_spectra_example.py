from gerg_plotting import ScatterPlot,data_from_df
import pandas as pd
import matplotlib.pyplot as plt

# Let's read in the example data
df = pd.read_csv('example_data/sample_tabs_data.csv')

for name,group in df.groupby('bin_depth'):
    data = data_from_df(group)

    freq,psd_u,psd_v,psd_w = data.calcluate_PSD(sampling_freq=48,segment_length=256)

    fig,axes = plt.subplots(nrows=3,figsize=(10,18),layout='constrained')

    scatter = ScatterPlot(data)
    scatter.power_spectra_density(freq=freq,psd=psd_u,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[0])
    scatter.power_spectra_density(freq=freq,psd=psd_v,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[1])
    scatter.power_spectra_density(freq=freq,psd=psd_w,highlight_freqs=[1/10, 1, 2],fig=fig,ax=axes[2])
    scatter.fig.suptitle(f'Auto-spectra of U Velocity (Bin Depth: {name} m)')
    plt.show()
    plt.clf()
