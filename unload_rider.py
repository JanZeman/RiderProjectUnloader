"""
Purpose:
---------
This script simulates the "Unload projects" feature of JetBrains Rider by creating a `.DotSettings.user` file.
By doing so, Rider will ignore these projects on startup, allowing it to start MUCH FASTER.
What this script does?
- It extracts project GUIDs the Visual Studio solution file (`.sln`)
- Encodes these keys to Rider format
- It also disables "Solution Wide Analysis" in Rider, further improving the startup performance.
- And finally generates the `*.sln.DotSettings.user` file that Rider expects.

How to Execute:
-------------------------------
- Place this script in the same directory as your Visual Studio solution (.sln) file.
- Run the script using Python: "python unload_rider.py <solution-file>.sln"

Notes:
------
- This script only needs to be run once, or whenever the solution file changes (e.g., projects are added or removed).
- It's recommended to close Rider before running the script to avoid any conflicts.
- Start Rider after running the script. It should start very fast and all project will be in their unloaded state.
- Decide which projects to load, typically by right-clicking on one of your application projects and selecting "Load Project with Dependencies" option.
- Optionally re-enable the "Solution Wide Analysis".
"""

import os
import sys
import xml.etree.ElementTree as ET
import re
import argparse
from xml.dom import minidom

# Set up argument parser
parser = argparse.ArgumentParser(description="Unload Rider projects by creating a .DotSettings.user file.")
parser.add_argument('solution', type=str, nargs='?', help="The Visual Studio solution file (.sln) to process")
args = parser.parse_args()

# Check if the solution argument is provided
if not args.solution:
    print("Error: The solution file (.sln) must be provided as an argument.")
    print("Usage: python unload_rider.py <solution-file>.sln")
    sys.exit(1)

# Use the solution file passed as an argument
solution = args.solution

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to your .sln file in the current directory
sln_file = os.path.join(current_directory, f'{solution}')

# Verify that the .sln file exists
if not os.path.exists(sln_file):
    print(f"Error: Solution file '{sln_file}' not found.")
    sys.exit(1)

# Path to your .sln.DotSettings.user file in the current directory
settings_file = os.path.join(current_directory, f'{solution}.DotSettings.user')

def extract_keys_from_solution_file(sln_file_path):
    keys = []
    with open(sln_file_path, 'r') as file:
        for line in file:
            # Match the correct GUID and project name
            match = re.search(r'Project\("\{[A-F0-9-]+\}"\) = "[^"]+", "([^"]+\\([^\\]+))\.csproj", "\{([A-F0-9-]+)\}"', line)
            if match:
                guid = match.group(3)
                # Extract the project name without the path or extension
                project_name = match.group(2)
                keys.append((guid, project_name))
    return keys

def encode_keys_to_rider_format(keys):
    modified_keys = []
    
    # Constants for encoding
    GUID_SEPARATOR = '_002D'  # ASCII hex code for '-'
    PROJECT_NAME_PREFIX = '_0023'  # ASCII hex code for '#'
    
    for guid, project_name in keys:
        # Print the original GUID and project name for debugging
        print(f"VS format: {guid}, NAME: {project_name}")

        # Encode the GUID to match Rider's format:
        # - Convert to lowercase
        # - Replace hyphens with GUID_SEPARATOR
        encoded_guid = guid.lower().replace('-', GUID_SEPARATOR)
        
        # Encode the project name to match Rider's format:
        # - Prepend PROJECT_NAME_PREFIX to the project name
        # - Replace any non-alphanumeric character with its ASCII hex code in uppercase
        encoded_project_name = re.sub(r'[\W]', lambda match: f"_{ord(match.group(0)):04X}", project_name)
        encoded_name = PROJECT_NAME_PREFIX + encoded_project_name
        
        # Combine the encoded GUID and project name into the final Rider key
        rider_key = f"{encoded_guid}{encoded_name}"
        
        # Print the encoded Rider key for debugging
        print(f"Rider key: {rider_key}\n")
        
        # Add the encoded key to the list of modified keys
        modified_keys.append(rider_key)
    
    return modified_keys

def pretty_print_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="\t", newl='\n')[23:]
    # Remove any newlines or whitespace just before the closing tag
    pretty_xml = re.sub(r'\s+</wpf:ResourceDictionary>$', '</wpf:ResourceDictionary>', pretty_xml)
    return pretty_xml

def add_solution_wide_analysis_setting(root):
    # Add the Solution-Wide Analysis setting
    ET.SubElement(root, 's:String', {
        'x:Key': "/Default/CodeInspection/Highlighting/AnalysisEnabled/@EntryValue"
    }).text = 'VISIBLE_FILES'

def create_rider_user_settings_xml_file(rider_keys, output_file_path):
    namespaces = {
        'x': "http://schemas.microsoft.com/winfx/2006/xaml",
        's': "clr-namespace:System;assembly=mscorlib",
        'ss': "urn:shemas-jetbrains-com:settings-storage-xaml",
        'wpf': "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    }

    root = ET.Element('wpf:ResourceDictionary', {
        'xmlns:x': namespaces['x'],
        'xmlns:s': namespaces['s'],
        'xmlns:ss': namespaces['ss'],
        'xmlns:wpf': namespaces['wpf'],
        'xml:space': "preserve"
    })

    # Add the Solution-Wide Analysis setting as the very first entry
    add_solution_wide_analysis_setting(root)

    # Add boolean entries for each project so it will not get loaded on Rider startup
    for key in rider_keys:
        ET.SubElement(root, 's:Boolean', {'x:Key': f"/Default/UnloadedProject/UnloadedProjects/={key}/@EntryIndexedValue"}).text = 'True'
    
    pretty_xml = pretty_print_xml(root)
    
    # Add the first line with xml:space="preserve"
    pretty_xml = f'<wpf:ResourceDictionary xml:space="preserve" xmlns:x="{namespaces["x"]}" xmlns:s="{namespaces["s"]}" xmlns:ss="{namespaces["ss"]}" xmlns:wpf="{namespaces["wpf"]}">\n' + pretty_xml.split('\n', 1)[1]
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

# Extract the keys from the solution file
extracted_keys = extract_keys_from_solution_file(sln_file)

# Sort the keys by GUID
extracted_keys.sort(key=lambda x: x[0].lower())

# Modify the keys to match Rider's encoding
rider_keys = encode_keys_to_rider_format(extracted_keys)

# Create the .DotSettings.user file
create_rider_user_settings_xml_file(rider_keys, settings_file)

print(f"Done! {len(rider_keys)} projects will be unloaded and 'Solution Wide Analysis' disabled.")
print("Please restart Rider, decide which projects to load and re-enable the Analysis manually :-)\n")