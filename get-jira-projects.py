import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
from release import parse_releases

def load_config():
    config_path = os.path.expanduser('jira_credentials.json')
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file at {config_path}")
        return None

def get_project_versions(project_key):
    """
    Retrieves all versions (releases) from the specified project using the Jira REST API.
    
    Args:
        project_key (str): The key of the project to retrieve versions from.
    
    Returns:
        A list of Release objects containing version information from the project.
    """
    url = f"{baseURL}/rest/api/3/project/{project_key}/versions"
    
    try:
        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            timeout=60
        )
        response.raise_for_status()
        return parse_releases(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving versions for project {project_key}: {str(e)}")
        return []

def write_releases_to_json(releases, project_key):
    """
    Writes the release data to a JSON file.
    
    Args:
        releases (list): A list of Release objects containing release information.
        project_key (str): The key of the project to use in the filename.
    """
    filename = f"{project_key.lower()}_releases.json"
    try:
        with open(filename, 'w') as file:
            json.dump([release.__dict__ for release in releases], file, indent=4, default=str)
        print(f"Release data for {project_key} successfully written to {filename}")
    except Exception as e:
        print(f"Error writing release data to file: {str(e)}")

def process_project(project_key):
    """
    Processes a single project: retrieves its versions and writes them to a JSON file.
    
    Args:
        project_key (str): The key of the project to process.
    """
    releases = get_project_versions(project_key)
    if releases:
        write_releases_to_json(releases, project_key)

config = load_config()
if not config:
    print("Failed to load configuration. Cannot proceed.")
    exit(1)

baseURL = config['jira_url']
auth = HTTPBasicAuth(config['username'], config['api_token'])

headers = {
    "Accept": "application/json"
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get-jira-projects.py <PROJECT_KEY>")
        sys.exit(1)
    
    project_key = sys.argv[1]
    process_project(project_key)