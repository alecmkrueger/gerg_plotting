# from gerg_plotting import CoveragePlot
import cmocean

from gerg_plotting.plotting_classes.coverage_plot import *

# Define labels for axes
xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
ylabels = ['Surface', 'Mid', 'Deep']

# Initialize plotter with default settings
plotter = CoveragePlot(
    figsize=(10, 6),
    xlabels=xlabels,
    ylabels=ylabels
)

# Define the colors we will use
colors = {
    "full_coverage":"#edf6f9",
    "point":"#008692",
    "parital_coverage":"#83c5be"
}

# Set default plotting parameters
plotter.config = {
    'label_fontsize': 12,
    'body_alpha': 0.8,
    'arrow_facecolor': 'coverage_color',
    'arrow_edgecolor': 'black',
    'arrow_linewidth': 1,
    'show_arrows': True,
    'label_background_alpha':0,
}

# Add coverages with cmocean colors
plotter.add_coverage(
    xrange=['Jan', 'Jun'],
    yrange=['Surface', 'Deep'],
    label='Full Coverage',
    body_hatch='/',
    body_color=colors['full_coverage'],
    label_position=(4.5,1),
    label_background_alpha=1,
    label_background_color=colors['full_coverage']
)

plotter.add_coverage(
    xrange='Mar',
    yrange='Surface',
    label='Point',
    body_color=colors["point"]
)

plotter.add_coverage(
    xrange=['Feb', 'Apr'],
    yrange=['Mid', 'Deep'],
    label='Partial Coverage',
    body_color=colors['parital_coverage'],
    label_position=(2.5,2),
)

plotter.plot(show_grid=True)
plotter.ax.set_title('Sample Coverage Plot')
