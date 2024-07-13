# assignment

Assignment Question :

LLM and RAG has been a hot topic around the world. We would like to track the public Github repos containing the llm and rag topics to gauge the growth and activity of the topic in the open source software scene. We can track the number of repos and the number of issues and PRs over time to get a general idea.


High-Level Solution Overview
In this assignment, you are tasked to develop a standard ETL/ELT solution. The high level steps involved are as follows:

Section A: ETL / ELT
1.Extract data from Github. You can create a Github API key and interact with Github REST API to fetch the data. You can use open source libraries such as GitHub - PyGithub/PyGithub: Typed interactions with the GitHub API v3 to make things easier.
 
2.Extract metadata of repositories, in incremental mode
a.Create as repositories table

3.  Extract issues info and PR information.
a. Create as issues_and_prs table
b. Bonus if you can do it in incremental mode

4. For both pipelines, perform first run and second run executions to prove that the incremental update logic is working. For example,
 a. For the repositories table, show that the number of repos after the second run is greater than after just the first run
 b. for the issues_and_prs table, show that the number of issues and prs for one or a few repos after the second run are greater than or equal to after just the first run

5. Implement data quality checks (DQCs) as you see fit

Section B: Analytics

As a Data Engineer, it’s also important to understand analytical needs downstream. For this section, you will be asked to perform a simple analytical aggregation. 

1. We would like to have a single chart (tool of your choice) to show the number of repos over time and number of issues and/or prs growth over time

2. List the top 5 repos with the most stars, top 5 repos with the most PRs and top 5 repos with the most issues


Here's a complete solution for tracking the growth and activity of public GitHub repositories containing the LLM and RAG topics. The solution is divided into three Python files:

elt_repository.py: Extract and load repository metadata.
elt_issues_prs.py: Extract and load issues and PR information.
etl_analytics.py: Perform analytics and generate visualizations.


How to Run :

Install dependencies: Ensure you have the required libraries installed:

pip install requests PyGithub pandas matplotlib sqlite3

Run the scripts:

Run elt_repository.py to extract and load repository metadata.
Run elt_issues_prs.py to extract and load issues and PR information.
Run etl_analytics.py to perform analytics and generate visualizations.



