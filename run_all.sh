#!/bin/bash

# Set variables for GitHub organization and token
ORG_NAME=$1
TOKEN=$2

# Check if both arguments are provided
if [ -z "$ORG_NAME" ] || [ -z "$TOKEN" ]; then
    echo "Usage: ./run_all.sh <org_name> <token>"
    exit 1
fi

# Step 1: Fetch repository summary
echo "Fetching repository summary..."
python fetch_repo_summary.py "$ORG_NAME" "$TOKEN"
if [ $? -ne 0 ]; then
    echo "Error fetching repository summary."
    exit 1
fi

# Step 2: Fetch repo tags and commit information
echo "Fetching repository details (tags and commits)..."
python fetch_repo_details.py "$TOKEN"
if [ $? -ne 0 ]; then
    echo "Error fetching repository details."
    exit 1
fi

# Step 3: Combine the data into a single JSON and CSV
echo "Combining repository data..."
python combine_repo_data.py
if [ $? -ne 0 ]; then
    echo "Error combining repository data."
    exit 1
fi

echo "All steps completed successfully!"
