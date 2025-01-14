from pathlib import Path
import ast

def get_function_info(content):
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node.lineno, ast.get_docstring(node)
    return None, None

def add_docstrings():
    examples_dir = Path('src/examples')
    example_files = examples_dir.glob('*_example.py')
    
    for file_path in example_files:
        with open(file_path, 'r') as f:
            content = f.read()
            
        image_path = file_path.with_suffix('.png')
        gif_path = file_path.with_suffix('.gif')
        output_path = gif_path if gif_path.exists() else image_path
        
        func_pos, existing_docstring = get_function_info(content)
        if func_pos:
            additional_content = f'''
    Source Code
    ~~~~~~~~~~
    .. literalinclude:: ../../../{file_path}
       :language: python

    Output
    ~~~~~~
    .. image:: ../../../{output_path}
       :width: 600
    '''
            
            if existing_docstring:
                # Remove closing quotes, add new content, and close quotes
                lines = content.splitlines()
                docstring_lines = existing_docstring.splitlines()
                
                # Find docstring end and insert new content
                for i, line in enumerate(lines):
                    if '"""' in line and i > func_pos:
                        lines[i] = additional_content + '\n    """'
                        break
                
                new_content = '\n'.join(lines)
            else:
                # Create new docstring
                lines = content.splitlines()
                new_docstring = f'''    """
    {file_path.stem.replace('_', ' ').title()}
    -----------{additional_content}
    """'''
                lines.insert(func_pos, new_docstring)
                new_content = '\n'.join(lines)
                
            with open(file_path, 'w') as f:
                f.write(new_content)

if __name__ == '__main__':
    add_docstrings()
