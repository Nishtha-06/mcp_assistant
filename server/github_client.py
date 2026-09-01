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
                "Github request timed out. Please try again."
            )

        except httpx.RequestError:
            raise GitHubAPIError(
                "Unable to connect to github. Please check your network."
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

        # Use the shared request method for consistent HTTP and network error handling.
        response = self._request("GET", url)
        return response.json()

    def search_repositories(self,query: str,limit: int = 10,page: int = 1) -> list:
        """Search GitHub repo using a search query."""

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100.")

        if page < 1:
            raise ValueError("Page number must be greater than 0.")

        url = f"{self.BASE_URL}/search/repositories"

        response = self._request(
            "GET",
            url,
            params={
                "q": query,
                "per_page": limit,
                "page": page,
            },
        )

        return response.json()["items"]

    # page selects which batch of results to retrieve, while limit controls how many results are returned per page.
    def list_issue(self,owner: str,repo: str,limit: int = 10,page: int = 1) ->list:
        """List issues from a GitHub repo"""

        self._validate_repo(owner, repo)

        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100.")

        if page < 1:
            raise ValueError("Page number must be greater than 0.")

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"

        # Use the shared request method for consistent HTTP and network error handling.
        response = self._request("GET", url,
                                params={"state": "open", "per_page": limit,"page": page})


        return response.json()

    def list_pull_requests(self,owner:str,repo:str,limit: int = 10,page:int = 1) -> list:
        """List open pull requests from github repo"""

        self._validate_repo(owner, repo)

        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100.")

        # Validate the requested page number before sending it to GitHub.
        if page < 1:
            raise ValueError("Page number must be a positive integer.")

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"

        # Use the shared request method for consistent HTTP and network error handling.
        response = self._request("GET", url,
                                params={"state": "open", "per_page": limit,"page": page})

        return response.json()

    def get_issue(self,owner:str,repo: str,issue_number: int) -> dict:
        """Get a specific issue from a GitHub repository."""

        self._validate_repo(owner,repo)

        if issue_number < 1:
            raise ValueError("Issue number must be a positive integer.")
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues/{issue_number}"

        #request one specific issue from GitHub API
        response = self._request("GET", url)

        return response.json()

    def get_pull_request(self,owner:str,repo:str,pull_number:int) -> dict:
        """Get a specific pull request from a Github repo"""
        self._validate_repo(owner,repo)

        if pull_number < 1:
            raise ValueError("Pull request number must be greater than 0.")

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"

        # request one specific pull request from the Github API.
        response = self._request("GET",url)

        return response.json()
