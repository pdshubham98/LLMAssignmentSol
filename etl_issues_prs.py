import os
from datetime import datetime
from github import Github
import pandas as pd

# Github API access token
github_token = os.getenv('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')
g = Github(github_token)

# Initialize data storage
issues_prs_data = []

# Function to fetch issues and PRs
def fetch_issues_prs(repo_full_name):
    repo = g.get_repo(repo_full_name)
    issues = repo.get_issues(state='all')
    for issue in issues:
        issues_prs_data.append({
            'repo_full_name': repo_full_name,
            'issue_pr_id': issue.id,
            'title': issue.title,
            'state': issue.state,
            'created_at': issue.created_at,
            'updated_at': issue.updated_at
        })

# Function to save issues and PRs data
def save_issues_prs_data():
    df = pd.DataFrame(issues_prs_data)
    df.to_csv('issues_and_prs.csv', index=False)

# Main function
def main():
    # Example repo_full_name
    repo_full_name = "pdshubham98/assignment"
    fetch_issues_prs(repo_full_name)
    save_issues_prs_data()

if __name__ == "__main__":
    main()
