"""
An example demonstrating some customization options for CoveragePlot.
"""

import matplotlib.pyplot as plt
import numpy as np
from gerg_plotting import CoveragePlot
import cmocean

# Define the axes labels
xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ylabels = ['Surface (0-100m)', 'Subsurface (100-500m)', 'Mid-depth (500-1000m)', 'Deep (1000-2000m)', 'Bottom (>2000m)']

# Initialize the coverage plot with custom figsize and labels
plotter = CoveragePlot(
    figsize=(14, 8),
    xlabels=xlabels,
    ylabels=ylabels,
    cmap='tab20'  # Use a colormap with more distinct colors
)

# ================================================================
# SECTION 1: Global Configuration
# ================================================================
# Set global configuration options that apply to all coverages
plotter.update_config(**{
    # CoveragePlotConfig options
    'horizontal_padding': 0.5,     # Padding on left and right of plot
    'vertical_padding': 0.5,       # Padding on top and bottom of plot
    
    # GridConfig options
    'grid_linewidth': 1.5,         # Width of grid lines
    'grid_linestyle': '--',        # Style of grid lines
    'grid_color': '#666666',       # Color of grid lines
    'grid_zorder': 1,              # Drawing order for grid
    
    # Basic CoverageConfig options
    'body_alpha': 0.8,             # Transparency of coverage bodies
    'body_linewidth': 1,           # Line width for coverage bodies
    'outline_edgecolor': 'black',  # Color of coverage outlines
    'outline_alpha': 0.9,          # Transparency of outlines
    'outline_linewidth': 1.5,      # Width of coverage outlines
    
    # Label options
    'label_fontsize': 11,          # Font size for labels
    'label_background_pad': 3,     # Padding around label background
    'label_background_linewidth': 1, # Width of label background border
    'label_background_alpha': 0.8, # Transparency of label background
    
    # Arrow options
    'arrow_tail_width': 0.06,      # Width of arrow tail
    'arrow_head_width': 0.15,      # Width of arrow head
    'arrow_zorder': 3,             # Drawing order for arrows
    'arrow_linewidth': 1,          # Width of arrow border lines
    'arrow_text_padding': 0.1,     # Padding between arrow and text
    'show_arrows': True,            # Whether to show extent arrows
})

# ================================================================
# SECTION 2: Basic Coverage Examples (Simple Configuration)
# ================================================================

# Example 1: Basic coverage with default styling
plotter.add_coverage(
    xrange=['Jan', 'Mar'],
    yrange=['Surface (0-100m)', 'Subsurface (100-500m)'],
    label='Basic Coverage'
)

# Example 2: Point coverage (single date/depth)
plotter.add_coverage(
    xrange='Apr',
    yrange='Mid-depth (500-1000m)',
    label='Point\nCoverage',
    body_color='#FF5733'  # Custom hex color
)

# Example 3: Coverage with custom positioning
plotter.add_coverage(
    xrange=['Jun', 'Aug'],
    yrange=['Deep (1000-2000m)', 'Bottom (>2000m)'],
    label='Custom Position',
    label_position=(7, 3.75)  # Position label at specific coordinates
)

# ================================================================
# SECTION 3: Advanced Coverage Styling
# ================================================================

# Example 4: Coverage with hatching
plotter.add_coverage(
    xrange=['Sep', 'Dec'],
    yrange=['Surface (0-100m)', 'Mid-depth (500-1000m)'],
    label='Hatched Coverage',
    body_color='#E6F7FF',          # Light blue background
    body_hatch='///',              # Diagonal hatching
    body_hatch_color='#0066CC',    # Dark blue hatch color
    hatch_linewidth=1.5,           # Width of hatch lines
    outline_linewidth=2,           # Thicker outline
    outline_edgecolor='#003366'    # Custom outline color
)

# Example 5: Gradient-filled coverage without arrows
plotter.add_coverage(
    xrange=['Feb', 'May'],
    yrange=['Mid-depth (500-1000m)', 'Bottom (>2000m)'],
    label='No Arrows',
    body_color=cmocean.cm.deep(0.7),  # Using cmocean colormap
    show_arrows=False,                # Disable arrows
    body_alpha=0.9,                   # High opacity
    outline_edgecolor='white',        # White outline
    outline_linewidth=2               # Thick outline
)

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
# plotter.save('coverage_plot_customization_example.png', dpi=300)
