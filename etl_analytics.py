import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATABASE = 'github_data.db'

# Function to get repository count over time
def get_repo_count_over_time():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('SELECT DATE(created_at) as date, COUNT(*) as count FROM repositories GROUP BY date', conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

# Function to get issues and PRs count over time
def get_issues_prs_count_over_time():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('SELECT DATE(created_at) as date, COUNT(*) as count FROM issues_and_prs GROUP BY date', conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

# Function to get top repositories by stars
def get_top_repos_by_stars():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('SELECT full_name, stargazers_count FROM repositories ORDER BY stargazers_count DESC LIMIT 5', conn)
    conn.close()
    return df

# Function to get top repositories by PRs
def get_top_repos_by_prs():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('''
        SELECT r.full_name, COUNT(*) as pr_count
        FROM repositories r
        JOIN issues_and_prs i ON r.id = i.repo_id
        WHERE i.is_pull_request = 1
        GROUP BY r.full_name
        ORDER BY pr_count DESC
        LIMIT 5
    ''', conn)
    conn.close()
    return df

# Function to get top repositories by issues
def get_top_repos_by_issues():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('''
        SELECT r.full_name, COUNT(*) as issue_count
        FROM repositories r
        JOIN issues_and_prs i ON r.id = i.repo_id
        WHERE i.is_pull_request = 0
        GROUP BY r.full_name
        ORDER BY issue_count DESC
        LIMIT 5
    ''', conn)
    conn.close()
    return df

# Function to plot analytics
def plot_analytics():
    repo_count_df = get_repo_count_over_time()
    issues_prs_count_df = get_issues_prs_count_over_time()
    
    plt.figure(figsize=(14, 7))

    plt.subplot(1, 2, 1)
    plt.plot(repo_count_df['date'], repo_count_df['count'], label='Repositories', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Repositories Over Time')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate(rotation=45)

    plt.subplot(1, 2, 2)
    plt.plot(issues_prs_count_df['date'], issues_prs_count_df['count'], label='Issues and PRs', color='orange', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Issues and PRs Over Time')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate(rotation=45)

    plt.tight_layout()
    plt.show()

    top_stars = get_top_repos_by_stars()
    top_prs = get_top_repos_by_prs()
    top_issues = get_top_repos_by_issues()

    print("Top 5 Repositories by Stars:")
    print(top_stars)
    print("\nTop 5 Repositories by PRs:")
    print(top_prs)
    print("\nTop 5 Repositories by Issues:")
    print(top_issues)

if __name__ == '__main__':
    plot_analytics()
