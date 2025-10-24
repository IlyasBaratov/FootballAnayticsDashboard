"""Fix imports by removing backEnd. prefix"""
import os
import re

def fix_imports(directory="."):
    for root, dirs, files in os.walk(directory):
        # Skip venv and pycache
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Replace from  with from 
                    content = re.sub(r'from backEnd\.', 'from ', content)
                    
                    # Only write if changed
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    fix_imports()
    print("Done!")
