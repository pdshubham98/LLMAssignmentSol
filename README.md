# GitHub Data Tracking and Analytics

Assignment Question :

LLM and RAG has been a hot topic around the world. We would like to track the public Github repos containing the llm and rag topics to gauge the growth and activity of the topic in the open source software scene. We can track the number of repos and the number of issues and PRs over time to get a general idea.

Solution Approach: ETL / ELT

1. Extract Data from GitHub:
To gather data from GitHub, we'll employ a GitHub API key for direct access to the GitHub REST API. This API key facilitates seamless interaction with GitHub's vast repository of open-source projects. We'll leverage libraries like PyGitHub to simplify our API interactions, ensuring efficient and effective data retrieval.

2. Extract Metadata of Repositories:
Our first step involves creating a dedicated repositories table. This table will serve as a repository for essential metadata such as repository names, descriptions, star ratings, creation dates, and other relevant details. This ensures we have a comprehensive view of each repository's characteristics.

3. Extract Issues and PR Information:
Next, we'll establish an issues_and_prs table designed to capture detailed information about issues and pull requests (PRs) across GitHub repositories. This includes critical details such as issue/PR titles, creation dates, statuses, and more. To optimize data tracking, we'll implement incremental updates within this table. This approach allows us to efficiently monitor and record changes over time, ensuring our data remains current and accurate.

4. Incremental Updates Verification:
To validate the effectiveness of our incremental update strategy, we'll conduct thorough verification checks. This involves comparing the counts of repositories and issues/PRs before and after subsequent data extraction runs. By doing so, we ensure that our pipeline effectively captures new data additions without duplications or omissions.

5. Implement Data Quality Checks (DQCs):
Data integrity is paramount. Hence, we'll implement rigorous Data Quality Checks (DQCs) throughout our ETL/ELT process. These checks will encompass verifying the presence of essential fields, validating data types, and ensuring the reasonableness of numerical values such as stars, PRs, and issues. By adhering to these standards, we maintain high-quality data that is reliable for downstream analysis and decision-making.



Section B: Analytics

1. Analytical Aggregation:
To gain insights into the growth and activity of GitHub repositories related to LLM and RAG topics, we'll perform analytical aggregation. Using a versatile tool such as matplotlib, we'll create visualizations that depict the trends in repository growth over time and the volume of issues and pull requests (PRs) submitted. These visualizations provide a clear overview of how these topics are evolving within the open-source community, helping us understand their prominence and engagement levels.

2. Top Repositories by Metrics:
Identifying the most influential repositories within the LLM and RAG domains is crucial. We'll compile lists of the top 5 repositories based on several key metrics:

  a. Stars: Highlighting repositories that have garnered the highest number of stars indicates popularity and community endorsement.

  b. PRs: Repositories with the most pull requests signify active collaboration and development efforts.

  c. Issues: Repositories with a significant number of issues showcase ongoing discussions, bug reports, and community involvement.

These metrics allow us to pinpoint repositories that are not only popular but also actively contributing to the advancement and discussion of LLM and RAG topics. By focusing on these top repositories, we can better understand their impact and relevance within the broader software development landscape.

# Instructions for Setup and Execution :

# Prerequisites:

GitHub API Key: 
Before proceeding, ensure you have obtained a GitHub API key from your GitHub account settings. This key will be necessary to interact with the GitHub REST API.

Python Libraries: 
Install necessary libraries using pip install command.

SQLite Database: 
Make sure SQLite is installed on your system to create and manage the SQLite database (github_data.db) where repository metadata and issue/PR information will be stored.



# Conclusion : 
This structured solution offers a robust framework for tracking GitHub repositories associated with LLM and RAG topics. By leveraging GitHub's API and Python libraries like PyGitHub, we ensure accurate extraction of repository metadata and issue/PR information. The implementation of incremental updates and data quality checks enhances reliability, supporting ongoing monitoring and analysis.

Customizable to meet specific business needs, this solution facilitates deep insights into repository growth and activity trends over time. The integration with SQLite for data management and visualization tools like matplotlib for analytics ensures comprehensive exploration of repository metrics.

By adopting this approach, organizations can effectively monitor and analyze open-source contributions related to LLM and RAG topics, leveraging data-driven decisions to drive innovation and strategic initiatives.

# ** Note :
Due to resource constraints (specifically cluster configuration limitations), the current implementation may encounter difficulties when fetching issues_and_prs for all repositories simultaneously. However, the underlying solution for extracting issues_and_prs data from repositories is robust and functional.

The pipeline has been designed to successfully retrieve metadata and other relevant information from repositories containing the keywords "llm" and "rag". It efficiently captures repository metadata and, where possible, issues and pull requests (PRs), demonstrating effective use of incremental updates to track changes over time.

While issues_and_prs extraction for all repositories is constrained by current resource limitations, the implemented pipeline remains reliable for individual repository queries and incremental updates.


