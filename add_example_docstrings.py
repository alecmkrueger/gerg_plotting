from pathlib import Path
import ast

def has_docstring(content):
    try:
        tree = ast.parse(content)
        return ast.get_docstring(tree) is not None
    except:
        return False

def add_docstrings():
    examples_dir = Path('examples')
    example_files = examples_dir.glob('*_example.py')
    
    for file_path in example_files:    
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        if not has_docstring(content):
            docstring = f'''"""
{file_path.stem.replace('_', ' ').title()}
===================================

Example description

"""
'''
            with open(file_path, 'w') as f:
                f.write(docstring + content)

if __name__ == '__main__':
    add_docstrings()
