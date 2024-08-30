from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
import copy  # Add this import
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

def filter_releases(releases, project_key):
    """
    Filters releases based on project-specific rules.
    
    Args:
        releases (list): A list of Release objects.
        project_key (str): The key of the project being processed.
    
    Returns:
        A tuple containing three filtered lists of Release objects:
        (non_nsbl_releases, nsbl_releases, pubs_releases) for CIS project,
        (releases, [], []) for other projects.
    """
    if project_key == "CIS":
        nsbl_releases = []
        pubs_releases = []
        non_nsbl_pubs_releases = []
        for release in releases:
            if "CIS" in release.name.upper():
                original_release = copy.deepcopy(release)
                stripped_name = release.name.lower().replace("cis", "").strip()
                release.name = stripped_name
                nsbl_releases.append(release)
                pub_release = copy.deepcopy(original_release)
                pub_release.name = stripped_name
                pubs_releases.append(pub_release)
                original_release.name = stripped_name
                non_nsbl_pubs_releases.append(original_release)
            elif release.name.replace(".", "").isdigit():
                pubs_release = copy.deepcopy(release)
                pubs_releases.append(pubs_release)
                nsbl_release = copy.deepcopy(release)
                nsbl_releases.append(nsbl_release)
                cis_release = copy.deepcopy(release)
                non_nsbl_pubs_releases.append(cis_release)
            elif "PUBS" in release.name.upper():
                modified_release = copy.deepcopy(release)
                modified_release.name = modified_release.name.lower().replace("pubs", "").strip()
                pubs_releases.append(modified_release)
            elif "nsbl" not in release.name.lower() and "pubs" not in release.name.lower():
                modified_release = copy.deepcopy(release)
                modified_release.name = modified_release.name.lower().replace("nsbl", "").strip()
                non_nsbl_pubs_releases.append(modified_release)
        
        # Sort all release lists by releaseDate (newest first)
        releases.sort(key=lambda x: x.releaseDate or datetime.min.date(), reverse=True)
        non_nsbl_pubs_releases.sort(key=lambda x: x.releaseDate or datetime.min.date(), reverse=True)
        nsbl_releases.sort(key=lambda x: x.releaseDate or datetime.min.date(), reverse=True)
        pubs_releases.sort(key=lambda x: x.releaseDate or datetime.min.date(), reverse=True)
        
        return non_nsbl_pubs_releases, nsbl_releases, pubs_releases
    
    # For other projects, sort releases by releaseDate (newest first)
    releases.sort(key=lambda x: x.releaseDate or datetime.min.date(), reverse=True)
    return releases, [], []

def write_releases_to_json(releases, filename):
    """
    Writes the release data to a JSON file.
    
    Args:
        releases (list): A list of Release objects containing release information.
        filename (str): The name of the file to write the data to.
    """
    try:
        with open(filename, 'w') as file:
            json.dump([release.__dict__ for release in releases], file, indent=4, default=str)
        print(f"Release data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing release data to file: {str(e)}")

def process_project(project_key):
    """
    Processes a single project: retrieves its versions, filters them, and writes them to JSON file(s).
    
    Args:
        project_key (str): The key of the project to process.
    """
    releases = get_project_versions(project_key)
    if releases:
        filtered_releases, nsbl_releases, pubs_releases = filter_releases(releases, project_key)
        write_releases_to_json(filtered_releases, f"{project_key.lower()}_releases.json")
        if project_key == "CIS":
            if nsbl_releases:
                write_releases_to_json(nsbl_releases, "nsbl_releases.json")
            if pubs_releases:
                write_releases_to_json(pubs_releases, "pubs_releases.json")

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
