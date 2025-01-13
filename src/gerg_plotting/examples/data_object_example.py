from gerg_plotting import Data, Variable, data_from_csv
import pandas as pd
import cmocean

def data_object_example():
    """
    Simple example showing the three main ways to create a data object
    """
    # Load data from CSV file
    df = pd.read_csv('example_data/sample_glider_data.csv')
    
    # Method 1: Directly from CSV file (Easiest method)
    data = data_from_csv('example_data/sample_glider_data.csv')
    print("1. Created data object from CSV file")
    
    # Method 2: Create variables first, then make data object (Most control)
    # Create temperature variable with specific settings
    temperature = Variable(
        name='temperature',
        data=data['temperature'].data,
        units='°C',
        cmap=cmocean.cm.thermal,  # Color scheme for plotting
        vmin=-10,  # Minimum value for color scale
        vmax=40    # Maximum value for color scale
    )
    
    # Create salinity variable with specific settings
    salinity = Variable(
        name='salinity',
        data=data['salinity'].data,
        units='PSU',
        cmap=cmocean.cm.haline,  # Special color scheme for salinity
        vmin=28,
        vmax=40
    )
    
    # Create new data object with our custom variables
    custom_data = Data(
        temperature=temperature,
        salinity=salinity
    )
    print("2. Created data object with custom variables")
    
    # Method 3: Add variables to existing data object
    # Create a new variable for Turner angle
    Turner_angle = Variable(
        name='Turner_angle',
        data=df['Turner_angle'],
        units='degrees',
    )
    
    # Add the new variable to our data object
    custom_data.add_custom_variable(Turner_angle)
    print("3. Added custom variable to existing data object")
    
    # Make a simple plot to show our data
    from gerg_plotting.plotting_classes.Histogram import Histogram
    plot = Histogram(custom_data)
    plot.plot('temperature')
    plot.save('example_plots/data_object_example.png')
    print("Created example plot: simple_temperature_histogram.png")

if __name__ == "__main__":
    data_object_example()