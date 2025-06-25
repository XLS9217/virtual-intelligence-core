import os

def list_all_files(base_path):
    for root, dirs, files in os.walk(base_path):
        # Skip hidden dirs and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for file in files:
            if not file.startswith("."):
                full_path = os.path.relpath(os.path.join(root, file), base_path)
                print(full_path)

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    print(f"Listing all files under module: {os.path.basename(current_dir)}\n")
    list_all_files(current_dir)
