import os

def print_directory_tree(path, indent=""):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                print(f"{indent}+-- {entry.name}")
                print_directory_tree(entry.path, indent + "    ")
            else:
                print(f"{indent}|-- {entry.name}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Directory Tree for: {current_dir}")
    print_directory_tree(current_dir)
