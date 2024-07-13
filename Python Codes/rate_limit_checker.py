import requests

# Constants
GITHUB_API_KEY = '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'
if not GITHUB_API_KEY:
    raise ValueError("GitHub API token not found. Please set the environment variable 'GITHUB_API_KEY'.")

HEADERS = {'Authorization': f'token {GITHUB_API_KEY}'}

def check_rate_limit():
    url = 'https://api.github.com/rate_limit'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        rate_limit_data = response.json()
        remaining = rate_limit_data['rate']['remaining']
        limit = rate_limit_data['rate']['limit']
        reset_time = rate_limit_data['rate']['reset']
        
        print(f"Remaining API calls: {remaining}/{limit}")
        print(f"Rate limit resets at: {reset_time} (UTC)")
    else:
        print(f"Failed to check rate limit: {response.status_code}, {response.text}")

if __name__ == '__main__':
    check_rate_limit()
