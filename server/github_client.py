# GitHub API Client: Handles communication with the GitHub REST API so the MCP tools can access GitHub data.
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

class GitHubAPIError(Exception):
    """Raise when the Github API returns an error."""

class GitHubClient:
    """Client for interacting with the GitHub REST API."""

    BASE_URL = "https://api.github.com"

    def __init__(self): #It runs automatically when you create an object.
        self.token = os.getenv("GITHUB_TOKEN")

        if not self.token:
            raise ValueError("GITHUB_TOKEN is not configured")

        self.header = {
            "Authorization": f"Bearer {self.token}",
            "Accept":"application/vnd.github+json",
        }


    def _validate_repo(self,owner: str,repo: str) -> None:
        """Validate GitHub repository owner and repository name."""
        if not owner or not owner.strip():
            raise ValueError("Repository owner cannot be empty.")
        if not repo or not repo.strip():
            raise ValueError("Repository name cannot be empty.")
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repository name must not contain '/'.")

    def get_repository(self,owner:str,repo:str) -> dict:
        """Get information about a github repository."""

        self._validate_repo(owner,repo)
        url = f"{self.BASE_URL}/repos/{owner}/{repo}" #https://api.github.com/repos/Nishtha-06/IntelliOrbit

        response = httpx.get(
            url,
            headers = self.header,
            timeout = 10.0,
        )

        if response.status_code != 200:
            raise GitHubAPIError(
                f"Github API Error: {response.status_code} - "
                f"{response.text}"
            )
        return response.json()

    def list_issue(self,owner: str,repo: str) ->list:
        """List issues from a GitHub repo"""

        self._validate_repo(owner, repo)

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"

        response = httpx.get(
            url,
            headers = self.header,
            params = {"state":"open"},
            timeout = 10.0,
        )

        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API error: {response.status_code} - "
                f"{response.text}"
            )

        return response.json()

    def list_pull_requests(self,owner:str,repo:str) -> list:
        """List pull requests from github repo"""

        self._validate_repo(owner, repo)

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"

        response = httpx.get(
            url,
            headers = self.header,
            params = {"state": "open"},
            timeout = 10.0,
        )

        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API error: {response.status_code} - "
                f"{response.text}"
            )

        return response.json()

