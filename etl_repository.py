import os
from datetime import datetime
from github import Github
import pandas as pd
import requests
import time

# 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

# GitHub API access token
GITHUB_API_KEY = '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'
if not GITHUB_API_KEY:
    raise ValueError("GitHub API token not found. Please set the environment variable 'GITHUB_API_KEY'.")

g = Github(GITHUB_API_KEY)

# Initialize data storage
repositories_data = []

# Function to fetch repositories
def fetch_repositories():
    query = "llm OR rag"
    try:
        repos = g.search_repositories(query=query)
        for repo in repos:
            repositories_data.append({
                'id': repo.id,
                'name': repo.name,
                'full_name': repo.full_name,
                'html_url': repo.html_url,
                'description': repo.description,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count
            })
        print(f"Fetched {len(repositories_data)} repositories.")
    except Exception as e:
        print(f"An error occurred while fetching repositories: {e}")

def fetch_data():
    url = 'https://api.github.com/search/repositories?q=llm+OR+rag'
    headers = {'Authorization': f'token {GITHUB_API_KEY}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()  # Attempt to decode JSON
        # Process your data here
        print(data)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except ValueError as val_err:
        print(f'JSON decoding error occurred: {val_err}')

fetch_data()

# Function to save repositories data
def save_repositories_data():
    if not repositories_data:
        print("No repository data to save.")
        return
    df = pd.DataFrame(repositories_data)
    df.to_csv('repositories.csv', index=False)
    print(f"Saved {len(repositories_data)} repositories to 'repositories.csv'.")

# Main function
def main():
    fetch_repositories()
    save_repositories_data()

if __name__ == "__main__":
    main()
