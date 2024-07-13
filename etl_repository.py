import requests
import sqlite3
import time
from datetime import datetime
from github import Github

# Constants
# GitHub API access token
GITHUB_API_KEY = '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'
if not GITHUB_API_KEY:
    raise ValueError("GitHub API token not found. Please set the environment variable 'GITHUB_API_KEY'.")

DATABASE = 'github_data.db'
SEARCH_QUERY = 'topic:llm topic:rag'
HEADERS = {'Authorization': f'token {GITHUB_API_KEY}'}

# Initialize GitHub API
g = Github(GITHUB_API_KEY)

# Function to create repositories table
def create_repositories_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS repositories')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY,
            name TEXT,
            full_name TEXT,
            html_url TEXT,
            description TEXT,
            created_at TEXT,
            updated_at TEXT,
            pushed_at TEXT,
            stargazers_count INTEGER,
            language TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch repositories from GitHub
def fetch_repositories(page=1, per_page=30):
    query = f"https://api.github.com/search/repositories?q={SEARCH_QUERY}&page={page}&per_page={per_page}"
    response = requests.get(query, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)  # Print the response content for debugging
        raise Exception(f"Error fetching repositories: {response.status_code}, {response.text}")

# Function to save repositories to database
def save_repositories(repos):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for repo in repos:
        cursor.execute('''
            INSERT OR REPLACE INTO repositories (
                id, name, full_name, html_url, description, created_at, updated_at, pushed_at, stargazers_count, language
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            repo['id'], repo['name'], repo['full_name'], repo['html_url'], repo['description'],
            repo['created_at'], repo['updated_at'], repo['pushed_at'], repo['stargazers_count'], repo['language']
        ))
    conn.commit()
    conn.close()

# Function to perform incremental update
def incremental_update():
    page = 1
    while True:
        print(f"Fetching page {page}...")
        try:
            repos_data = fetch_repositories(page)
            if 'items' not in repos_data or len(repos_data['items']) == 0:
                print(f"No more data found on page {page}.")
                break
            save_repositories(repos_data['items'])
            print(f"Page {page} fetched and saved.")
            page += 1
            time.sleep(2)  # To avoid hitting rate limits
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def check_rate_limit():
    url = 'https://api.github.com/rate_limit'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        rate_limit_data = response.json()
        remaining = rate_limit_data['rate']['remaining']
        reset_time = datetime.fromtimestamp(rate_limit_data['rate']['reset'])
        print(f"Remaining API calls: {remaining}")
        print(f"Rate limit resets at: {reset_time}")
    else:
        print(response.text)
        raise Exception(f"Error fetching rate limit: {response.status_code}, {response.text}")

def count_repositories():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM repositories')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def data_quality_check_repositories():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check for missing values in critical columns
        cursor.execute('SELECT COUNT(*) FROM repositories WHERE name IS NULL OR full_name IS NULL')
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"WARNING: Found {null_count} records with missing 'name' or 'full_name'.")

        # Check for duplicates based on unique constraints (if any)
        cursor.execute('SELECT COUNT(*) FROM repositories GROUP BY name, full_name HAVING COUNT(*) > 1')
        duplicate_count = cursor.fetchone()
        if duplicate_count:
            print(f"WARNING: Found {duplicate_count[0]} duplicate records based on 'name' and 'full_name'.")
        else:
            print("No duplicate records found based on 'name' and 'full_name'.")

        # Additional checks can be added as needed

    except Exception as e:
        print(f"Error during data quality checks: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    check_rate_limit()
    create_repositories_table()

    # Perform first run of incremental update
    incremental_update()
    count_after_first_run = count_repositories()
    print(f"Number of repositories after the first run: {count_after_first_run}")

    # Perform second run of incremental update
    incremental_update()
    count_after_second_run = count_repositories()
    print(f"Number of repositories after the second run: {count_after_second_run}")

    # Compare counts
    if count_after_second_run > count_after_first_run:
        print("Incremental update logic for repositories table is working.")
    else:
        print("Incremental update logic for repositories table needs review.")

    # Run data quality checks
    data_quality_check_repositories()
