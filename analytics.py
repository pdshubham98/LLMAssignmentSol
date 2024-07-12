import pandas as pd
import matplotlib.pyplot as plt

# Load data
repositories = pd.read_csv('repositories.csv')
issues_prs = pd.read_csv('issues_and_prs.csv')

# Convert dates to datetime
repositories['created_at'] = pd.to_datetime(repositories['created_at'])
issues_prs['created_at'] = pd.to_datetime(issues_prs['created_at'])

# Analytics: Repositories over time
repositories_over_time = repositories.groupby(pd.Grouper(key='created_at', freq='M')).size()

# Analytics: Issues and PRs over time
issues_prs_over_time = issues_prs.groupby(pd.Grouper(key='created_at', freq='M')).size()

# Plotting repositories over time
plt.figure(figsize=(10, 6))
repositories_over_time.plot(kind='line', marker='o', linestyle='-', color='b', label='Repositories')
plt.title('Number of Repositories Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Repositories')
plt.legend()
plt.grid(True)
plt.savefig('repositories_over_time.png')
plt.show()

# Top 5 repositories by stars
top_stars = repositories.nlargest(5, 'stars')[['full_name', 'stars']]

# Top 5 repositories by PRs
top_prs = issues_prs['repo_full_name'].value_counts().nlargest(5)

# Top 5 repositories by issues
top_issues = issues_prs[issues_prs['state'] == 'open']['repo_full_name'].value_counts().nlargest(5)

print("Top 5 Repositories by Stars:")
print(top_stars.to_string(index=False))

print("\nTop 5 Repositories by Pull Requests:")
print(top_prs)

print("\nTop 5 Repositories by Issues:")
print(top_issues)
