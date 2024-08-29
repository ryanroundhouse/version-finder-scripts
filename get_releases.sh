#!/bin/bash

# Set the project keys
PROJECT_KEYS=("CIS" "MC" "CSR" "BLR" "A7")

# Run the Python script for each project key
for PROJECT_KEY in "${PROJECT_KEYS[@]}"; do
    echo "Fetching releases for project: $PROJECT_KEY"
    python3 get-jira-projects.py "$PROJECT_KEY"
done

echo "All project releases have been fetched and saved."