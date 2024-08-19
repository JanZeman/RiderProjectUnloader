#!/bin/bash

# Purpose:
# --------
# This script is a convenience wrapper to execute the Python script "unload_rider.py".
# It checks for the existence of the Python script and runs it to generate the necessary
# .DotSettings.user file for JetBrains Rider to unload specific projects on startup.

# How to Run:
# -----------
# 1. Ensure this script is executable by running:
#    chmod +x unload_rider.sh
# 
# 2. Execute the script:
#    ./unload_rider.sh

# Define the path to the Python script
PYTHON_SCRIPT="unload_rider.py"

# Define the solution file to be processed
SOLUTION_FILE="UnloadRiderProjects.sln"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found!"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install it and try again."
    exit 1
fi

# Run the Python script with the hardcoded solution file
echo "Running $PYTHON_SCRIPT with solution file '$SOLUTION_FILE'..."
python3 $PYTHON_SCRIPT "$SOLUTION_FILE"