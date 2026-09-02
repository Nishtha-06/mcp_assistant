# MCP Server: Exposes GitHub operations as MCP tools that an MCP client/AI can call.

from mcp.server.fastmcp import FastMCP #FastMCPServer is a convenient way to create an MCP server in Python.
from server.github_client import GitHubClient

mcp = FastMCP("GitHub MCP Assistant") # Create an instance of the FastMCPServer class.  

github = GitHubClient() # Create an instance of the GitHubClient class.

@mcp.tool() # the function immediately below this decorator will be a tool in the MCP server.
def hello(name: str) -> str: 
    """Return a greeting message."""
    return f"Hello, {name}!" 

@mcp.tool()
def get_repo(owner:str,repo:str) -> dict:
    """Get information about a GitHub repository"""
    return github.get_repository(owner,repo)

@mcp.tool()
def search_repositories(query: str,limit: int = 10,page: int = 1) -> list: 
    """Search GitHub repositories."""
    return github.search_repositories(query,limit,page)

@mcp.tool()
def list_issues(owner: str, repo: str,limit: int = 10,page: int = 1) -> list:
    """List open issues from a GitHub repository."""
    return github.list_issue(owner, repo,limit,page)


@mcp.tool()
def list_pull_requests(owner: str, repo: str,limit: int=10,page: int = 1) -> list:
    """List open pull requests from a GitHub repository."""
    return github.list_pull_requests(owner, repo,limit,page)

@mcp.tool()
def get_issue(owner:str,repo: str,issue_number: int) -> dict:
    """Get a specific issue from github repo"""

    return github.get_issue(owner,repo,issue_number)

@mcp.tool()
def get_pull_request(owner: str,repo: str,pull_number: int) -> dict:
    """Get a specific pull request from a GitHub repository."""

    # Expose specific pull request lookup as an MCP tool.
    return github.get_pull_request(owner, repo, pull_number)

if __name__ == "__main__": # This block ensures that the server runs only when this script is executed directly(python server.py), not when imported as a module.
    mcp.run()

