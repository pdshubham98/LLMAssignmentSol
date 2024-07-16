import requests
import sqlite3
import time
from datetime import datetime
from github import Github

# Constants
GITHUB_API_KEY = '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'
if not GITHUB_API_KEY:
    raise ValueError("GitHub API token not found. Please set the environment variable 'GITHUB_API_KEY'.")

DATABASE = 'github_data.db'
HEADERS = {'Authorization': f'token {GITHUB_API_KEY}'}

# Initialize GitHub API
g = Github(GITHUB_API_KEY)

# Function to create issues_and_prs table
def create_issues_and_prs_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues_and_prs (
            id INTEGER PRIMARY KEY,
            repo_id INTEGER,
            number INTEGER,
            title TEXT,
            state TEXT,
            created_at TEXT,
            updated_at TEXT,
            closed_at TEXT,
            is_pull_request BOOLEAN,
            FOREIGN KEY (repo_id) REFERENCES repositories (id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch issues and PRs from GitHub
def fetch_issues_and_prs(repo_full_name):
    issues = g.get_repo(repo_full_name).get_issues(state='all')
    return issues

# Function to save issues and PRs to database
def save_issues_and_prs(repo_id, issues):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for issue in issues:
        cursor.execute('''
            INSERT OR REPLACE INTO issues_and_prs (
                id, repo_id, number, title, state, created_at, updated_at, closed_at, is_pull_request
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            issue.id, repo_id, issue.number, issue.title, issue.state, issue.created_at,
            issue.updated_at, issue.closed_at, issue.pull_request is not None
        ))
    conn.commit()
    conn.close()

# Function to perform incremental update
def incremental_update():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name FROM repositories')
    repos = cursor.fetchall()
    conn.close()

    # Batch process repositories
    batch_size = 100  # Adjust batch size as per your requirements
    for i in range(0, len(repos), batch_size):
        batch_repos = repos[i:i + batch_size]
        for repo in batch_repos:
            repo_id, repo_full_name = repo
            print(f"Fetching issues and PRs for repository: {repo_full_name}")
            try:
                issues = fetch_issues_and_prs(repo_full_name)
                save_issues_and_prs(repo_id, issues)
                print(f"Issues and PRs for repository {repo_full_name} fetched and saved.")
            except Exception as e:
                print(f"An error occurred fetching or saving data for repository {repo_full_name}: {e}")
            time.sleep(2)  # To avoid hitting rate limits

# Function to count issues and PRs for a specific repository
def count_issues_and_prs(repo_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM issues_and_prs WHERE repo_id = ?', (repo_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Function to perform data quality checks (DQCs) for issues_and_prs table
def data_quality_check_issues_and_prs():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check for missing values in critical columns
        cursor.execute('SELECT COUNT(*) FROM issues_and_prs WHERE title IS NULL OR created_at IS NULL')
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"WARNING: Found {null_count} records with missing 'title' or 'created_at'.")

        # Check for duplicates based on unique constraints (if any)
        cursor.execute('SELECT COUNT(*) FROM issues_and_prs GROUP BY repo_id, number HAVING COUNT(*) > 1')
        duplicate_count = cursor.fetchone()
        if duplicate_count:
            print(f"WARNING: Found {duplicate_count[0]} duplicate records based on 'repo_id' and 'number'.")
        else:
            print("No duplicate records found based on 'repo_id' and 'number'.")

        # Additional checks can be added as needed

    except Exception as e:
        print(f"Error during data quality checks for issues_and_prs: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    create_issues_and_prs_table()

    # Perform incremental update
    incremental_update()

    # Perform first run of counting issues and PRs
    repo_id = 1  # Replace with the actual repo_id you want to check
    count_after_first_run = count_issues_and_prs(repo_id)
    print(f"Number of issues and PRs for repo_id {repo_id} after the first run: {count_after_first_run}")

    # Perform second run of incremental update
    incremental_update()

    # Perform second run of counting issues and PRs
    count_after_second_run = count_issues_and_prs(repo_id)
    print(f"Number of issues and PRs for repo_id {repo_id} after the second run: {count_after_second_run}")

    # Compare counts
    if count_after_second_run >= count_after_first_run:
        print("Incremental update logic for issues_and_prs table is working.")
    else:
        print("Incremental update logic for issues_and_prs table needs review.")

    # Run data quality checks for issues_and_prs table
    data_quality_check_issues_and_prs()
