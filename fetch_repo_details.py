import requests
import json
import sys
import os

# Accept GitHub token as command-line argument
if len(sys.argv) != 2:
    print("Usage: python fetch_repo_details.py <token>")
    sys.exit(1)

token = sys.argv[1]

# Authorization header with token
headers = {'Authorization': f'token {token}'}

# Directories for saving intermediate data
tags_dir = 'repo_tags'
commits_dir = 'repo_commits'

# Input file for repository summary data
summary_filename = 'repo_summary.json'

# Ensure directories exist
os.makedirs(tags_dir, exist_ok=True)
os.makedirs(commits_dir, exist_ok=True)

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

# Fetch and save tags for each repository
def fetch_and_save_repo_tags(repositories, headers, tags_dir):
    all_tags_data = {}
    for repo in repositories:
        full_repo_name = repo['full_name']
        filename = f"{tags_dir}/{full_repo_name.replace('/', '_')}_tags.json"
        
        # Check if tags for this repo have already been fetched
        if os.path.exists(filename):
            print(f"Skipping tags for {full_repo_name}, already saved.")
            continue
        
        try:
            # Fetch the tags
            tags_url = f'https://api.github.com/repos/{full_repo_name}/tags'
            response = requests.get(tags_url, headers=headers)
            response.raise_for_status()
            tags = response.json()
            all_tags_data[full_repo_name] = [tag['name'] for tag in tags]
            # Save tags to file
            save_to_file(all_tags_data[full_repo_name], filename)
            print(f"Saved tags for {full_repo_name} to {filename}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching tags for {full_repo_name}: {http_err}")
        except Exception as err:
            print(f"Error occurred while fetching tags for {full_repo_name}: {err}")

    return all_tags_data

# Fetch and save commit info for each repository
def fetch_and_save_repo_commits(repositories, headers, commits_dir):
    all_commits_data = {}
    for repo in repositories:
        full_repo_name = repo['full_name']
        filename = f"{commits_dir}/{full_repo_name.replace('/', '_')}_commit.json"
        
        # Check if commit info for this repo has already been fetched
        if os.path.exists(filename):
            print(f"Skipping commit info for {full_repo_name}, already saved.")
            continue
        
        try:
            # Fetch the last commit
            commits_url = f'https://api.github.com/repos/{full_repo_name}/commits?per_page=1'
            response = requests.get(commits_url, headers=headers)
            response.raise_for_status()
            commit_data = response.json()
            if commit_data:
                latest_commit = commit_data[0]
                all_commits_data[full_repo_name] = {
                    'last_commit_user': latest_commit['commit']['committer']['name'],
                    'last_commit_date': latest_commit['commit']['committer']['date']
                }
            else:
                all_commits_data[full_repo_name] = {'last_commit_user': 'Unknown', 'last_commit_date': 'Unknown'}
            
            # Save commit data to file
            save_to_file(all_commits_data[full_repo_name], filename)
            print(f"Saved commit info for {full_repo_name} to {filename}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching commits for {full_repo_name}: {http_err}")
        except Exception as err:
            print(f"Error occurred while fetching commits for {full_repo_name}: {err}")

    return all_commits_data

# Load repository summary data
repositories = load_from_file(summary_filename)
if not repositories:
    print(f"Error: {summary_filename} not found. Please run fetch_repo_summary.py first.")
    sys.exit(1)

# Fetch tags and commit info for each repository, saving per repo
repo_tags = fetch_and_save_repo_tags(repositories, headers, tags_dir)
repo_commits = fetch_and_save_repo_commits(repositories, headers, commits_dir)

print("Detailed repository information has been fetched and saved.")
