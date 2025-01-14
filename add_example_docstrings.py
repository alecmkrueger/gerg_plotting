from pathlib import Path
import ast

def has_docstring(content):
    try:
        tree = ast.parse(content)
        return ast.get_docstring(tree) is not None
    except:
        return False

def add_docstrings():
    examples_dir = Path('src/examples')
    example_files = examples_dir.glob('*_example.py')
    
    for file_path in example_files:
        # Check for both PNG and GIF outputs
        plot_path = file_path.parent.joinpath('example_plots')
        image_path = plot_path.joinpath(file_path.with_suffix('.png').name)
        gif_path = plot_path.joinpath(file_path.with_suffix('.gif').name)
        
        # Use GIF path if it exists, otherwise use PNG path
        output_path = gif_path if gif_path.exists() else image_path
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        if not has_docstring(content):
            docstring = f'''    """
    {file_path.stem.replace('_', ' ').title()}
    -----------

    Source Code
    ~~~~~~~~~~
    .. literalinclude:: ../../../{file_path}
    :language: python

    Output
    ~~~~~~
    .. image:: ../../../{output_path}
    :width: 600

    """
    '''
            with open(file_path, 'w') as f:
                f.write(docstring + content)

if __name__ == '__main__':
    add_docstrings()
