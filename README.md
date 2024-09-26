# GitHub Repository Data Fetcher

This repository contains scripts that help fetch repository information from a GitHub organization, retrieve detailed data such as tags and commits for each repository, and then combine this data into a JSON file and CSV file for easy consumption.

## Scripts Overview

1. **`fetch_repo_summary.py`**: Fetches summary information for all repositories in a GitHub organization and saves it to a file (`repo_summary.json`).
2. **`fetch_repo_details.py`**: Fetches detailed information (tags and commit history) for each repository listed in `repo_summary.json` and saves it to individual JSON files in the `repo_tags/` and `repo_commits/` directories.
3. **`combine_repo_data.py`**: Combines the summary, tags, and commit information into a single JSON file (`combined_repo_data.json`) and CSV file (`combined_repo_data.csv`).
4. **`run_all.sh`**: A Bash script that runs all the above scripts in sequence, ensuring that all necessary data is fetched and processed into the final output.
5. **`dockerRun.sh`**: A script to build and run the Docker container for easier development.

## Docker Setup (Optional but Recommended for Easier Development)

If you prefer to use Docker for a consistent development environment, this repository provides a `Dockerfile` and a `dockerRun.sh` script to simplify the setup.

### Building the Docker Image

Before running the scripts with Docker, you need to build the Docker image:

```bash
docker build -t repocleanup:latest .
```

This will create a Docker image named `repocleanup:latest` with all the necessary dependencies.

### Running the Docker Container

Once the image is built, you can use the `dockerRun.sh` script to run the container interactively:

```bash
./dockerRun.sh
```

This script runs the container with appropriate settings, mounts the current working directory to `/workspace` inside the container, and opens an interactive shell where you can run the Python scripts as usual.

### `dockerRun.sh` Contents:

```bash
#!/bin/bash

# Build the Docker image if it doesn't exist
docker build -t repocleanup:latest .

# Run the Docker container
docker run --rm -it \
    --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
    --name repocleanup \
    -v $(pwd):/workspace \
    -w /workspace \
    repocleanup:latest
```

## How to Run the Scripts

### 1. Running the Full Pipeline

You can run the entire process of fetching repository data, details, and combining the results by executing the `run_all.sh` script:

```bash
./run_all.sh <org_name> <github_token>
```

- **`<org_name>`**: The name of the GitHub organization whose repositories you want to analyze.
- **`<github_token>`**: Your personal access token for GitHub.

Example:

```bash
./run_all.sh trendscenter ghp_yourgithubtokenhere
```

This will:
1. Fetch a summary of all repositories in the organization and save it to `repo_summary.json`.
2. Fetch tags and commit information for each repository and save them in `repo_tags/` and `repo_commits/` directories.
3. Combine all data into `combined_repo_data.json` and `combined_repo_data.csv`.

### 2. Running Inside the Docker Container

If you're using Docker, first run the container interactively:

```bash
./dockerRun.sh
```

Once inside the container, you can run the same scripts as you would on your local machine:

```bash
./run_all.sh <org_name> <github_token>
```

This method ensures a consistent environment with all dependencies pre-installed, making development and execution simpler.

## Outputs

- **`repo_summary.json`**: Contains summary data for each repository in the organization.
- **`repo_tags/`**: Contains tag information for each repository.
- **`repo_commits/`**: Contains commit information for each repository.
- **`combined_repo_data.json`**: The final JSON output, combining repository summary, tags, and commits.
- **`combined_repo_data.csv`**: The final CSV output, which can be opened in Excel or other spreadsheet tools.

## Troubleshooting

- If any script fails during execution, it will print an error message and stop. You can re-run the process using the `run_all.sh` script, and it will continue from where it left off by skipping already processed repositories.
  
- Ensure that your GitHub token has the necessary permissions to read repositories and access commit history.


### Notes:
- This README assumes that users may want to use Docker for a more streamlined and consistent development process.
- The `dockerRun.sh` script builds the Docker image if it doesn't already exist, then runs the container interactively.
