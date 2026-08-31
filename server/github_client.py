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

    def _handle_response_error(self,response: httpx.Response) -> None:
        """Convert GitHub HTTP errors into self application errors."""

        if response.status_code == 401:
            raise GitHubAPIError("GitHub authentication failed.")
        if response.status_code == 403:
            raise GitHubAPIError("GitHub access denied or API rate limit exceeded.")
        if response.status_code == 404:
            raise GitHubAPIError("GitHub repository or resource was not found.")
        if response.status_code >= 500:
            raise GitHubAPIError("GitHub is currently unavailable. Please try again later.")
        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API request failed with status {response.status_code}."
            )

    def _request(self,method: str,url: str,**kwargs) -> httpx.Response: #method likes GET, POST etc, url is GitHub URL, **kwargs = It allows us to pass additional request options.like params={"state": "open"} for issues
        """Send a GitHub API request and Hnadle network errors."""

        try:
            response = httpx.request(
                method,
                url,
                headers = self.header,
                timeout = 10.0, # If GitHub doesn't respond within about 10 seconds, httpx can raise a timeout exception.
                **kwargs,
            )
        except httpx.TimeoutException:
            raise GitHubAPIError(
                "Github request time out. Please try again."
            )

        except httpx.RequestError:
            raise GitHubAPIError(
                "Unable to connect to github. Please check your nextwork."
            )

        self._handle_response_error(response)

        return response

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

        self._handle_response_error(response)
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

        self._handle_response_error(response)

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

        self._handle_response_error(response)

        return response.json()

