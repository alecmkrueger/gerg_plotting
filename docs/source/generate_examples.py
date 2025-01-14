import os
from pathlib import Path

def generate_plot_directives():
    # Path to examples directory
    examples_dir = Path('../../src/examples')
    output_file = Path('examples.rst')
    
    # Create RST content
    rst_content = ["Examples\n========\n\n"]
    
    # Find all Python files in examples directory
    for py_file in examples_dir.glob('*.py'):
        # Get relative path
        rel_path = py_file.relative_to(Path(''))
        
        # Add section header using filename
        section_name = py_file.stem.replace('_', ' ').title()
        rst_content.append(f"{section_name}\n{'-' * len(section_name)}\n\n")
        
        # Add plot directive
        rst_content.append(f".. plot:: {rel_path}\n\n")

    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(rst_content))

if __name__ == '__main__':
    generate_plot_directives()
