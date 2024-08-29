from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Release:
    self: str
    id: str
    name: str
    archived: bool
    released: bool
    projectId: int
    description: Optional[str] = None
    startDate: Optional[date] = None
    releaseDate: Optional[date] = None
    userStartDate: Optional[str] = None
    userReleaseDate: Optional[str] = None
    overdue: Optional[bool] = None

    def __post_init__(self):
        # Convert date strings to date objects
        if isinstance(self.startDate, str):
            self.startDate = date.fromisoformat(self.startDate)
        if isinstance(self.releaseDate, str):
            self.releaseDate = date.fromisoformat(self.releaseDate)

def parse_releases(json_data):
    releases = []
    for item in json_data:
        release = Release(
            self=item['self'],
            id=item['id'],
            name=item['name'],
            archived=item['archived'],
            released=item['released'],
            projectId=item['projectId'],
            description=item.get('description'),
            startDate=item.get('startDate'),
            releaseDate=item.get('releaseDate'),
            userStartDate=item.get('userStartDate'),
            userReleaseDate=item.get('userReleaseDate'),
            overdue=item.get('overdue')
        )
        releases.append(release)
    return releases

# Example usage:
if __name__ == "__main__":
    import json

    # Load the JSON data from file
    with open('cis_releases.json', 'r') as file:
        json_data = json.load(file)

    # Parse the releases
    releases = parse_releases(json_data)

    # Example: Print details of the first release
    if releases:
        first_release = releases[0]
        print(f"Name: {first_release.name}")
        print(f"Release Date: {first_release.releaseDate}")
        print(f"Description: {first_release.description}")