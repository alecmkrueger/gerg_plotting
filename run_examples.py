from pathlib import Path
import importlib.util
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Set backend to non-interactive before importing any plotting

def run_example(file_path):
    print(f"\nRunning example: {file_path.name}")
    
    # Store current working directory
    original_dir = os.getcwd()
    
    # Change to examples directory
    os.chdir(file_path.parent)
    
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path.name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_path.stem] = module
    spec.loader.exec_module(module)
    
    # Restore original working directory
    os.chdir(original_dir)
    print(f"Completed: {file_path.name}")

def main():
    examples_dir = Path("docs/examples")
    output_dir = Path("example_plots")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Get all Python files in examples directory
    example_files = list(examples_dir.glob("*.py"))
    
    print(f"Found {len(example_files)} example files")
    
    # Run each example
    for example_file in example_files:
        run_example(example_file)
        
    print("\nAll examples completed. Check example_plots directory for outputs.")

if __name__ == "__main__":
    main()
