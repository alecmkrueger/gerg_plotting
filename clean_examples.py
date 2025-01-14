import os
import re

examples_dir = "examples"

# Walk through all files in examples directory
for root, _, files in os.walk(examples_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            
            # Read file content
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Remove function definitions
            content = re.sub(r'def\s+\w+\s*\([^)]*\)\s*:', '', content)
            
            # Remove if __name__ == '__main__' block and everything after it
            content = re.sub(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:.*$', '', content, flags=re.DOTALL)
            
            # Remove first level of indentation (4 spaces or tab) from each line
            lines = content.split('\n')
            deindented_lines = []
            for line in lines:
                if line.startswith('    '):  # Remove 4 spaces
                    deindented_lines.append(line[4:])
                elif line.startswith('\t'):  # Remove tab
                    deindented_lines.append(line[1:])
                else:
                    deindented_lines.append(line)
            content = '\n'.join(deindented_lines)
            
            # Clean up extra blank lines
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # Write cleaned content back
            with open(filepath, 'w') as f:
                f.write(content.strip() + '\n')
