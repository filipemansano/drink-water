import os

def print_dir_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = '|   ' * level + '|-- '
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '|   ' * (level + 1) + '|-- '
        for f in files:
            print(f"{subindent}{f}")

print_dir_tree('source')