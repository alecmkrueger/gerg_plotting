"""
Coverage Plot Example
===================================

How to create a coverage plot.


"""
from gerg_plotting import CoveragePlot
from gerg_plotting.tools.tools import custom_legend_handles

import matplotlib.pyplot as plt

cmap = plt.get_cmap('tab20')
domains = ['Regional_Local', 'All', 'Local', 'Basin_Regional', 'Basin_Local', 'Basin', 'Regional']
colors_light = [cmap(15),cmap(5),cmap(3),cmap(1),'yellow','pink','gold']

colors = colors_light
domain_colors = {key:value for key,value in zip(domains,colors)}

hatch_styles = ['/', '\\', '|', '-', 'o', 'O', '.', '*',
                '//', '\\\\', '||', '--', '++', 'xx', 'oo', 'OO', '..', '**', '/o', 
                '\\|', '|*', '-\\', '+o', 'x*', 'o-', 'O|', 'O.', '*-']

domain_hatches = {key:value for key,value in zip(domains,hatch_styles)}
# Define the x and y labels
xlabels = ['Seconds','Minutes','Hours','Days','Weeks','Months','Years','Decades']
ylabels = ['Surface','10-100\nMeters','100-500\nMeters','Below 500\nMeters','Benthic']

# Define the default plotting parameters
plotting_kwargs = {'arrow_facecolor':'hatch_color','body_color':'none','label_fontsize':9,'label_background_pad':0.75,
                'label_background_color':'hatch_color','arrow_linewidth':0.75,'hatch_linewidth':4,'outline_linewidth':1.25,
                'show_arrows':False}

# Init the coverage plotter
plotter = CoveragePlot(figsize=(12,6),xlabels=xlabels,ylabels=ylabels,plotting_kwargs=plotting_kwargs)
# All Depths
plotter.add_coverage(['Hours','Decades'],['Surface','Benthic'],label='Agency',label_position=(4,3.3),hatch_color=domain_colors['All'],hatch=domain_hatches['All'])
plotter.add_coverage(['Seconds','Decades'],['Surface','Benthic'],label='Academic',label_position=(3.5,2),hatch_color=domain_colors['All'],hatch=domain_hatches['All'])
plotter.add_coverage(['Days','Months'],['Surface','Benthic'],label='Marine Services',label_position=(4.5,1.7),hatch_color=domain_colors['Regional_Local'],hatch=domain_hatches['Regional_Local'])
plotter.add_coverage(['Days','Years'],['Surface','Benthic'],label='Regulatory',label_position=(4.5,2.3),hatch_color=domain_colors['Regional_Local'],hatch=domain_hatches['Regional_Local'])
plotter.add_coverage(['Days','Decades'],['Surface','Benthic'],label='Oil and Gas',label_position=(4.5,3),hatch_color=domain_colors['All'],hatch=domain_hatches['All'])
plotter.add_coverage(['Months','Years'],['Surface','Benthic'],label='Fisheries',label_position=(6,2.75),hatch_color=domain_colors['Regional_Local'],hatch=domain_hatches['Regional_Local'])
plotter.add_coverage(['Hours','Weeks'],['Surface','Benthic'],label='Disaster',label_position=(4,2.75),hatch_color=domain_colors['All'],hatch=domain_hatches['All'])
# Surface
plotter.add_coverage(['Hours','Days'],[-0.5,-0.5],label='Search and Rescue',hatch_color=domain_colors['Local'],hatch=domain_hatches['Local'])
plotter.add_coverage(['Days','Decades'],[0.25,0.25],label='Wind and Algal Blooms',hatch_color=domain_colors['Local'],hatch=domain_hatches['Local'])
# 10-100m
plotter.add_coverage(['Months','Decades'],['Surface','100-500 Meters'],label='CCUS',label_position=(6,0.775),hatch_color=domain_colors['Local'],hatch=domain_hatches['Local'])
plotter.add_coverage(['Hours','Weeks'],[0.65,0.65],label='Hurricane Forcasting',hatch_color=domain_colors['All'],hatch=domain_hatches['All'])
plotter.add_coverage(['Days','Years'],[1,1],label='Hypoxia',hatch_color=domain_colors['Regional_Local'],hatch=domain_hatches['Regional_Local'])

plotter.add_coverage('Decades',['Surface','Benthic'],label='Climate\nScience',label_position=(7.5,1.7),hatch_color=domain_colors['Basin_Regional'],hatch=domain_hatches['Basin_Regional'])
plotter.add_coverage(['Weeks','Months'],[-0.5,-0.5],label='Shipping',hatch_color=domain_colors['Basin'],hatch=domain_hatches['Basin'])
plotter.add_coverage(['Days','Years'],[-0.15,-0.15],label='Recreational',label_position=(4.5,-0.025),hatch_color=domain_colors['Basin'],hatch=domain_hatches['Basin'])

plotter.plot(show_grid=False)

handles = custom_legend_handles(domain_colors.keys(),domain_colors.values(),hatches=domain_hatches.values(),color_hatch_not_background=True)
plotter.fig.legend(handles=handles,bbox_to_anchor=(0.254, 0.46),framealpha=1,title='Domains',handleheight=2, handlelength=3)

plotter.fig.tight_layout()

<<<<<<< Updated upstream
plotter.save('example_plots/coverage_plot_example.png',dpi=600,bbox_inches='tight')
=======
# Example 6: Coverage with custom label background
plotter.add_coverage(
    xrange=['Jul', 'Oct'],
    yrange=['Subsurface (100-500m)', 'Deep (1000-2000m)'],
    label='Custom Label BG',
    body_color='#F2F3F4',             # Light gray body
    label_background_color='#4A235A',  # Purple background
    label_fontsize=12,                # Larger font
    label_background_alpha=1.0,       # Fully opaque background
    label_background_pad=5,           # Extra padding around text
    label_font_color='white',         # White text
    body_min_height=0.5               # Minimum height for coverage area
)

# ================================================================
# SECTION 4: Arrow Customization
# ================================================================

# Example 7: Coverage with custom arrows
plotter.add_coverage(
    xrange=['Jan', 'Jun'],
    yrange='Bottom (>2000m)',
    label='Custom Arrows',
    body_color='#FFCC33',           # Orange-yellow body
    arrow_facecolor='#66CC33',      # Green arrows
    arrow_edgecolor='black',        # Black arrow outline
    arrow_linewidth=1.5,            # Thicker arrow outline
    arrow_tail_width=0.08,          # Wider arrow tail
    arrow_head_width=0.18,          # Wider arrow head
    arrow_text_padding=0.15         # More space between text and arrows
)

# Example 8: Coverage with arrows matching body color
plotter.add_coverage(
    xrange=['Aug', 'Dec'],
    yrange='Surface (0-100m)',
    label='Matched Arrows',
    body_color='#9966CC',           # Purple body
    arrow_facecolor='coverage_color', # Arrows same as body color
    arrow_edgecolor='white',        # White arrow outline
    arrow_linewidth=1,              # Medium arrow outline
    outline_alpha=0.5               # Semi-transparent outline
)

# ================================================================
# SECTION 5: Special Cases and Combinations
# ================================================================

# Example 9: Transparent body with only outline
plotter.add_coverage(
    xrange=['Feb', 'Nov'],
    yrange=['Deep (1000-2000m)', 'Bottom (>2000m)'],
    label='Outline Only',
    body_color='none',              # Transparent body
    body_alpha=0,                   # Fully transparent
    outline_edgecolor='#CC0033',    # Red outline
    outline_linewidth=3,            # Very thick outline
    outline_alpha=1.0,              # Fully opaque outline
    label_background_color='white', # White label background
    label_background_alpha=0.9      # Nearly opaque background
)

# Example 10: Combination of hatching and special arrows
plotter.add_coverage(
    xrange=['Apr', 'Sep'],
    yrange=['Surface (0-100m)', 'Subsurface (100-500m)'],
    label='Combined Styles',
    body_color='#E8F8F5',           # Light teal background
    body_hatch='xx',                # Cross hatching
    body_hatch_color='#117A65',     # Dark teal hatch
    hatch_linewidth=1,              # Medium hatch lines
    outline_edgecolor='#0E6655',    # Teal outline
    arrow_facecolor='#F1C40F',      # Yellow arrows
    arrow_edgecolor='#B7950B',      # Dark yellow arrow outline
    arrow_linewidth=1.5,            # Thicker arrow outline
    label_fontsize=13,              # Larger label
    label_background_color='white', # White background
    label_background_alpha=0.8      # Semi-transparent background
)

# ================================================================
# SECTION 6: Finalize and Display
# ================================================================

# Generate the plot
plotter.plot(show_grid=True)

# Add title and customize the plot further
plotter.ax.set_title('Comprehensive CoveragePlot Customization Example', fontsize=16, pad=20)

# Add explanatory text as an annotation
explanation_text = (
    "This example demonstrates the various customization options available in CoveragePlot.\n"
    "Customize: colors, hatches, arrows, labels, transparency, outlines, and more."
)
plotter.fig.text(0.5, 0.01, explanation_text, ha='center', fontsize=12)

# Adjust layout to make room for annotation
plotter.fig.tight_layout(rect=[0, 0.05, 1, 0.98])

# Display the plot
plotter.show()

# Save to file
plotter.save('example_plots/coverage_plot_example.png', dpi=300)
