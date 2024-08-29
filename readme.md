# Jira Project Release Fetcher

This script automates the process of fetching release information for multiple Jira projects.

## Description

The `get_releases.sh` script iterates through a predefined list of Jira project keys and calls a Python script (`get-jira-projects.py`) for each project. The Python script fetches the release information for the specified project from Jira and saves it to a JSON file.

## Prerequisites

- Bash shell
- Python 3
- `requests` library for Python (can be installed via `pip install requests`)
- Jira account with appropriate permissions to access project information
- `jira_credentials.json` file with Jira authentication details

## Setup

1. Ensure you have Python 3 installed on your system.
2. Install the required Python library:
   ```
   pip install requests
   ```
3. Create a `jira_credentials.json` file in the same directory as the scripts with the following structure:
   ```json
   {
     "jira_url": "https://your-jira-instance.atlassian.net",
     "username": "your-email@example.com",
     "api_token": "your-jira-api-token"
   }
   ```
4. Place the `get_releases.sh`, `get-jira-projects.py`, and `release.py` files in the same directory.

## Usage

1. Make the script executable:
   ```
   chmod +x get_releases.sh
   ```
2. Run the script:
   ```
   ./get_releases.sh
   ```

## Customization

To modify the list of projects for which to fetch releases, edit the `PROJECT_KEYS` array in `get_releases.sh`:
