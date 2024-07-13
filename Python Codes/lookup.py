import sqlite3

DATABASE = 'github_data.db'

def fetch_all_repositories():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM issues_and_prs')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    repositories = fetch_all_repositories()
    for repo in repositories:
        print(repo)
