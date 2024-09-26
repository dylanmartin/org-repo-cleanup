import os
import json
import csv
import sys

# Input files and directories
summary_filename = 'repo_summary.json'
tags_dir = 'repo_tags'
commits_dir = 'repo_commits'

# Output files
combined_json_filename = 'combined_repo_data.json'
combined_csv_filename = 'combined_repo_data.csv'

def load_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def combine_repo_data(summary_filename, tags_dir, commits_dir):
    combined_data = []
    
    # Load the repository summary
    repo_summary = load_from_file(summary_filename)
    if not repo_summary:
        print(f"Error: {summary_filename} not found.")
        sys.exit(1)
    
    # Combine summary data with tags and commits
    for repo in repo_summary:
        full_repo_name = repo['full_name'].replace('/', '_')
        
        # Load tags data
        tags_filename = f"{tags_dir}/{full_repo_name}_tags.json"
        tags = load_from_file(tags_filename) or []
        
        # Load commit data
        commits_filename = f"{commits_dir}/{full_repo_name}_commit.json"
        commit_info = load_from_file(commits_filename) or {'last_commit_user': 'Unknown', 'last_commit_date': 'Unknown'}
        
        # Combine the data into a single entry
        combined_data.append({
            'name': repo.get('name'),
            'full_name': repo.get('full_name'),
            'html_url': repo.get('html_url'),
            'description': repo.get('description'),
            'created_at': repo.get('created_at'),
            'updated_at': repo.get('updated_at'),
            'pushed_at': repo.get('pushed_at'),
            'private': repo.get('private'),
            'archived': repo.get('archived'),
            'disabled': repo.get('disabled'),
            'forks_count': repo.get('forks_count'),
            'open_issues_count': repo.get('open_issues_count'),
            'stargazers_count': repo.get('stargazers_count'),
            'watchers_count': repo.get('watchers_count'),
            'language': repo.get('language'),
            'size': repo.get('size'),
            'topics': ','.join(repo.get('topics', [])),  # Converting topics list to a comma-separated string
            'default_branch': repo.get('default_branch'),
            'visibility': repo.get('visibility'),
            'last_commit_user': commit_info.get('last_commit_user'),
            'last_commit_date': commit_info.get('last_commit_date'),
            'tags': ','.join(tags)  # Converting tags list to a comma-separated string
        })
    
    return combined_data

def save_combined_data_as_json(combined_data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, ensure_ascii=False, indent=4)

def save_combined_data_as_csv(combined_data, filename):
    # Extract the keys for CSV columns from the first entry
    keys = combined_data[0].keys() if combined_data else []
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(combined_data)

# Main function to process and save data
def main():
    combined_data = combine_repo_data(summary_filename, tags_dir, commits_dir)
    
    # Save combined data as JSON
    save_combined_data_as_json(combined_data, combined_json_filename)
    print(f"Combined data saved to {combined_json_filename}")
    
    # Save combined data as CSV
    save_combined_data_as_csv(combined_data, combined_csv_filename)
    print(f"Combined data saved to {combined_csv_filename}")

if __name__ == '__main__':
    main()
