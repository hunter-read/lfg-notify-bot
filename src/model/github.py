import datetime
import json
import os
from github import Github, Auth


class GitHubManager:
    """A class for uploading to github."""

    def __init__(self):
        self.__client: client = self.__get_client()

    def __del__(self):
        self.__client.close()

    def __get_client(self) -> client:
        """Return a github client."""
        auth = Auth.Token(os.environ.get("GITHUB_ACCESS_TOKEN"))
        return Github(auth=auth)

    def upload(self, data: dict, object_name: str) -> None:
        repo = __client.get_repo(os.environ.get("GITHUB_STATISTICS_REPO"))
        contents = repo.get_contents(f"/public/{object_name}")
        repo.update_file(contents.path, f"Update {object_name} - {datetime.datetime.now().strftime('%Y-%m-%d')}", json.dumps(data), contents.sha, branch="main")
