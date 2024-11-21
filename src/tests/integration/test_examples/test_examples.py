import pytest
import glob
import importlib
import os
import inspect
from pathlib import Path

original_working_dir = os.getcwd()

# Examples path
examples_path = Path(__file__).parent.parent.parent.parent.joinpath('gerg_plotting','examples')

# Example py files
example_py_files = examples_path.rglob('*py')


@pytest.mark.slow
@pytest.mark.example
class TestExamples:
    """
    Pytest class to dynamically test all example functions.
    """

    def setup(self):
        """
        Set up class-level variables for dynamic test discovery.
        Dynamically configure paths for imports.
        """
        

        # Define the base dir
        self.base_dir = examples_path

        # Change the working directory
        os.chdir(self.base_dir)

        # Set the example data directory (to be accessed by example plotting functions)
        self.example_data_dir = self.base_dir.joinpath("example_data")

        # Set the example plot output directory
        self.example_plots_dir = self.base_dir.joinpath("example_plots")

        # Ensure the example data directory is accessible by the plotting functions
        if not self.example_data_dir.exists():
            raise FileNotFoundError(f"Example data directory {self.example_data_dir} not found.")
        
    
    def tear_down(self):
        os.chdir(original_working_dir)
        

    def remove_old_plot(self,example_file:str):
        [os.remove(file) for file in self.example_plots_dir.rglob(f'{Path(example_file).stem}.*')]


    @pytest.mark.parametrize("example_file", example_py_files, ids=lambda file: Path(file).name)
    def test_examples(self, example_file):
        """
        Dynamically test each example function.
        """
        self.setup()
        # Get the module name (file name without extension)
        module_name = Path(example_file).stem
        # module_name = os.path.splitext(os.path.basename(example_file))[0]
        module_path = f"gerg_plotting.examples.{module_name}"

        # Import the module dynamically
        module = importlib.import_module(module_path)

        # Get the function dynamically
        func = getattr(module, module_name, None)

        # Check that the function exists and is callable
        assert func is not None, f"{module_name} function does not exist in {example_file}"
        assert inspect.isfunction(func), f"{module_name} is not a function in {example_file}"

        # Remove existing plot
        self.remove_old_plot(str(example_file))

        # Call the function (the actual test)
        func()

        # Check if the module function output a matching image
        list_of_plots = [file.stem for file in self.example_plots_dir.rglob("*")]
        assert module_name in list_of_plots, f"Plot for {module_name} was not created."

        self.tear_down()
