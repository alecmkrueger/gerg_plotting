import unittest
import glob
import importlib
import os
import inspect
import sys
import pytest

@pytest.mark.example
class TestExamples(unittest.TestCase):
    """
    Unittest class to dynamically test all example functions.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class-level variables for dynamic test discovery.
        Dynamically configure paths for imports.
        """
        # Base path for the `gerg_plotting/src` folder
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

        # Ensure the base path is in the module search path
        sys.path.insert(0, base_dir)

        # Directory containing examples
        cls.examples_dir = os.path.join(base_dir, "gerg_plotting/examples")
        cls.example_files = glob.glob(os.path.join(cls.examples_dir, "*.py"))

        # Set the example data directory (to be accessed by example plotting functions)
        cls.example_data_dir = os.path.join(base_dir, "gerg_plotting/examples/example_data")

        # Ensure the example data directory is accessible by the plotting functions
        if not os.path.exists(cls.example_data_dir):
            raise FileNotFoundError(f"Example data directory {cls.example_data_dir} not found.")


    def test_examples(self):
        """
        Dynamically test each example function.
        """
        self.assertGreater(len(self.example_files),1)
        for example_file in self.example_files:
            # Get the module name (file name without extension)
            module_name = os.path.splitext(os.path.basename(example_file))[0]
            module_path = f"gerg_plotting.examples.{module_name}"

            with self.subTest(module=module_name):
                try:
                    # Import the module dynamically
                    module = importlib.import_module(module_path)

                    # Get the function dynamically
                    func = getattr(module, module_name, None)

                    # Check that the function exists and is callable
                    self.assertIsNotNone(func, f"{module_name} function does not exist in {example_file}")
                    self.assertTrue(inspect.isfunction(func), f"{module_name} is not a function in {example_file}")

                    # Call the function (the actual test)
                    func()

                except Exception as e:
                    self.fail(f"Test for {module_name} failed with error: {e}")

