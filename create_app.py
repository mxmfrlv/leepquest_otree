#!/usr/bin/env python3
"""
Script to:
1. Copy a 'leepquest' folder, rename it, and replace occurrences of 'leepquest'
   in the __init__.py file with the new name
2. Update settings.py to add the new app to SESSION_CONFIGS
"""

import os
import sys
import shutil
import re

def update_settings_file(source_folder, dest_folder):
    """
    Update the settings.py file to add the new app to SESSION_CONFIGS
    """
    settings_path = 'settings.py'
   
    if not os.path.isfile(settings_path):
        print(f"Warning: '{settings_path}' file not found.")
        return False
   
    print(f"Updating '{settings_path}' to add the new app...")
   
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
   
    # Find the SESSION_CONFIGS section using regex to handle multiline cases
    session_configs_pattern = r'SESSION_CONFIGS\s*=\s*\[(.*?)\]'
    match = re.search(session_configs_pattern, content, re.DOTALL)
   
    if match:
        # Check if the app is already in SESSION_CONFIGS
        app_pattern = rf"['\"]({dest_folder})['\"]"
        if re.search(app_pattern, match.group(1)):
            print(f"App '{dest_folder}' already exists in SESSION_CONFIGS.")
            return True
            
        # Extract the existing SESSION_CONFIGS content
        existing_configs = match.group(1)
        
        # Determine the indentation style from existing configs
        # Default to 4 spaces if we can't determine
        indent_match = re.search(r'^\s+', existing_configs.lstrip('\n'))
        indent = indent_match.group(0) if indent_match else '    '
        
        # Create a new dict entry for the new app with matching indentation
        new_app_config = f"""
{indent}dict(
{indent}    name='{dest_folder}',
{indent}    app_sequence=['{dest_folder}'],
{indent}    num_demo_participants=1,
{indent}),"""
       
        # Add the new config at the beginning of the list
        updated_configs = new_app_config + existing_configs
       
        # Replace the original SESSION_CONFIGS content with the updated one
        updated_content = content.replace(match.group(0), f"SESSION_CONFIGS = [{updated_configs}]")
       
        with open(settings_path, 'w', encoding='utf-8', newline='') as f:
            f.write(updated_content)
       
        return True
    else:
        print(f"Warning: Could not find SESSION_CONFIGS in {settings_path}")
        return False

def main():
    # Define the source folder name as a variable
    SOURCE_FOLDER = "leepquest"

    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("No app name provided.")
        user_input = input("Please enter a name for the new app: ")
        
        # Check if the user input is empty
        if not user_input.strip():
            print(f"Warning: No destination folder name provided.")
            print(f"Usage: {os.path.basename(sys.argv[0])} destination_folder_name")
            sys.exit(1)
        else:
            # Continue with the provided value
            print(f"Using value {user_input} as the new app's name")
            # Set the destination folder name from the argument
            DEST_FOLDER = user_input.strip()
    else:
        # Continue with the command line argument
        print(f"Using argument {sys.argv[1]} as the new app's name")
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
    
    with open(dest_init_path, 'w', encoding='utf-8', newline='') as f:
        f.write(updated_content)

    # Rename the excel file
    source_path = os.path.join(DEST_FOLDER, f"{SOURCE_FOLDER}.xlsx")
    destination_path = os.path.join(DEST_FOLDER, f"{DEST_FOLDER}.xlsx")
    
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        print(f"Renamed Excel file from {SOURCE_FOLDER}.xlsx to {DEST_FOLDER}.xlsx")
    else:
        print(f"Warning: Excel file {SOURCE_FOLDER}.xlsx not found in the new app directory.")

    # Update settings.py to add the new app to SESSION_CONFIGS
    if update_settings_file(SOURCE_FOLDER, DEST_FOLDER):
        print(f"Updated settings.py to include the new app '{DEST_FOLDER}'.")
    else:
        print(f"Failed to update settings.py.")

    print(f"Successfully copied and updated '{SOURCE_FOLDER}' to '{DEST_FOLDER}'.")

if __name__ == "__main__":
    main()