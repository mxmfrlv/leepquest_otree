#!/usr/bin/env python3
"""
Script to copy a 'leepquest' folder, rename it, and replace occurrences of 'leepquest'
in the __init__.py file with the new name.
"""

import os
import sys
import shutil
import re

def main():
    # Define the source folder name as a variable
    SOURCE_FOLDER = "leepquest"

    # Check if an argument is provided
    if len(sys.argv) < 2:
        print(f"Warning: No destination folder name provided.")
        print(f"Usage: {os.path.basename(sys.argv[0])} destination_folder_name")
        sys.exit(1)

    # Set the destination folder name from the argument
    DEST_FOLDER = sys.argv[1]

    # Check if source folder exists
    if not os.path.isdir(SOURCE_FOLDER):
        print(f"Warning: Source folder '{SOURCE_FOLDER}' does not exist.")
        sys.exit(1)

    # Check if __init__.py exists in the source folder
    init_path = os.path.join(SOURCE_FOLDER, "__init__.py")
    if not os.path.isfile(init_path):
        print(f"Warning: '__init__.py' file not found in the source folder.")
        sys.exit(1)

    # Check if the NAME_IN_URL line exists in __init__.py
    target_line = f"NAME_IN_URL = '{SOURCE_FOLDER}'"
    found_line = False
    
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if target_line in content:
            found_line = True
    
    if not found_line:
        print(f"Warning: \"{target_line}\" line not found in __init__.py")
        sys.exit(1)

    # Create destination folder if it exists, otherwise remove it and recreate
    if os.path.exists(DEST_FOLDER):
        shutil.rmtree(DEST_FOLDER)
    
    # Copy the folder, ignoring __pycache__
    def ignore_pycache(dir, files):
        return ['__pycache__']
    
    print(f"Copying files from {SOURCE_FOLDER} to {DEST_FOLDER}...")
    shutil.copytree(SOURCE_FOLDER, DEST_FOLDER, ignore=ignore_pycache)

    # Update the NAME_IN_URL line in __init__.py
    dest_init_path = os.path.join(DEST_FOLDER, "__init__.py")
    print(f"Updating NAME_IN_URL in __init__.py...")
    
    with open(dest_init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = content.replace(target_line, f"NAME_IN_URL = '{DEST_FOLDER}'")
    
    with open(dest_init_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # Rename the excel file
    source_path = os.path.join(DEST_FOLDER, f"{SOURCE_FOLDER}.xlsx")
    destination_path = os.path.join(DEST_FOLDER, f"{DEST_FOLDER}.xlsx")
    shutil.move(source_path, destination_path)


    print(f"Successfully copied and updated '{SOURCE_FOLDER}' to '{DEST_FOLDER}'.")

if __name__ == "__main__":
    main()