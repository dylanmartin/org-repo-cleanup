import requests
import json
import sys
import os

# Accept organization name and token as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python fetch_repo_summary.py <org_name> <token>")
    sys.exit(1)

org_name = sys.argv[1]
token = sys.argv[2]

# GitHub API URL for organization repositories (including archived repos)
base_url = f'https://api.github.com/orgs/{org_name}/repos?per_page=100&type=all&include_archived=true'

# Authorization header with token
headers = {'Authorization': f'token {token}'}

# Output file for summary data
summary_filename = 'repo_summary.json'

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def fetch_repo_summary(url, headers):
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        page_data = response.json()
        
        # Filter the fields we want for each repo
        for repo in page_data:
            repos.append({
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "pushed_at": repo.get("pushed_at"),
                "private": repo.get("private"),
                "archived": repo.get("archived"),
                "disabled": repo.get("disabled"),
                "forks_count": repo.get("forks_count"),
                "open_issues_count": repo.get("open_issues_count"),
                "stargazers_count": repo.get("stargazers_count"),
                "watchers_count": repo.get("watchers_count"),
                "language": repo.get("language"),
                "size": repo.get("size"),
                "topics": repo.get("topics", []),
                "default_branch": repo.get("default_branch"),
                "visibility": repo.get("visibility")
            })
        
        print(f"Fetched {len(page_data)} repositories")
        # Move to the next page if available
        url = response.links.get('next', {}).get('url')

    return repos

# Fetch the repository list and save summary data
repos = fetch_repo_summary(base_url, headers)
save_to_file(repos, summary_filename)
print(f"Repository summary information saved to {summary_filename}.")
