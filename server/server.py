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
def list_issues(owner: str, repo: str) -> list:
    """List open issues from a GitHub repository."""
    return github.list_issue(owner, repo)


@mcp.tool()
def list_pull_requests(owner: str, repo: str) -> list:
    """List open pull requests from a GitHub repository."""
    return github.list_pull_requests(owner, repo)

if __name__ == "__main__": # This block ensures that the server runs only when this script is executed directly(python server.py), not when imported as a module.
    mcp.run()

