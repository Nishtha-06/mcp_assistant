# MCP Client: Connects to the GitHUb MCP server and allows the client to discover and call MCP tools.

import asyncio #asyncio is Python's library for working with asynchronous programming.(Instead of blocking everything while waiting, we use asynchronous functions.)
import json # We need json so the large GitHub response can be converted into readable output.

from mcp import ClientSession, StdioServerParameters # ClientSession = represents the conversation/session between your MCP client and MCP server.
# StdioServerParameters = used to configure the connection between the MCP client and the MCP server.
from mcp.client.stdio import stdio_client # stdio = standard input/output. stdio_client = a function that sets up the MCP client to communicate with the MCP server using standard input/output streams.

server_params = StdioServerParameters(
    command="uv",
    args = ["run","python","-m","server.server"],
) 

async def main():
    """Connect to the MCP server and list available tools."""

    #nested context managers
    async with stdio_client(server_params) as (read,write): #creates a connection to your MCP server using standard input/output (stdio).
        # write → used to send messages to the server, read → used to receive messages from the server
        async with ClientSession(read,write) as session: # take those read,write channels and create an MCP client session.

            await session.initialize()

            tools = await session.list_tools() #list all the tools available on the MCP server.

            print("\nAvailable MCP tools:")
            print(f"Total tools: {len(tools.tools)}")

            await interactive_menu(session) 

async def call_tool(session,tool_name: str,arguments: dict):
    """Call an MCP tool and return its result."""
    result = await session.call_tool(
        tool_name,
        arguments = arguments,
    )

    return result

def get_result_data(result):
    """Extract the actual data returned from MCP tool."""

    if result.isError:
        if result.content:
            for content in result.content:
                if hasattr(content,"text"): #hasattr() = checks if the content object has a 'text' attribute.
                    return {"error": content.text}
        return None
    
    if not result.content:
        return None

    data = []
    for content in result.content:
        if hasattr(content,"text"):
            data.append(json.loads(content.text))

    if len(data) == 1:
        return data[0] # If there's only one item in the data list, return that single item.
    return data # If there are multiple items in the data list, return the entire list.

   

def print_result(result):
    """Print an MCP tool result in a readable JSON format."""

    data = get_result_data(result)

    if data is None:
        print("No data returned from the tool.")
        return

    if "error" in data:
        print(f"Error: {data['error']}")
        return

    print("\nResult: ")
    print(json.dumps(data, indent=2)) #dumps(data, indent=2) = converts the Python dictionary back into a JSON string with indentation for better readability.


# Format GitHub repository search results for readable terminal output.

def format_search_results(result):
    """Format repository search results into a concise terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No search results returned.")
        return

    print("\nSearch Results")
    print("==================")

    for index, repo in enumerate(data, start=1):
        print(f"\n{index}. {repo['full_name']}")
        print(f"   Description: {repo.get('description') or 'No description'}")
        print(f"   Stars: {repo.get('stargazers_count', 0)}")
        print(f"   Forks: {repo.get('forks_count', 0)}")
        print(f"   URL: {repo['html_url']}")

def format_repository_result(result):
    """Format repository information for terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No repository data returned.")
        return

    print("\nRepository")
    print("==================")
    print(f"Name: {data.get('full_name', 'N/A')}")
    print(f"Description: {data.get('description') or 'No description'}")
    print(f"Stars: {data.get('stargazers_count', 0)}")
    print(f"Forks: {data.get('forks_count', 0)}")
    print(f"Open Issues: {data.get('open_issues_count', 0)}")
    print(f"Language: {data.get('language') or 'N/A'}")
    print(f"URL: {data.get('html_url', 'N/A')}")

# Format GitHub issue results for readable terminal output.

def format_issues_result(result):
    """Format issue results for terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No issues returned.")
        return

    print("\nIssues")
    print("==================")

    for index, issue in enumerate(data, start=1):
        print(f"\n{index}. #{issue.get('number', 'N/A')} - {issue.get('title', 'No title')}")
        print(f"   State: {issue.get('state', 'N/A')}")
        print(f"   Author: {issue.get('user', {}).get('login', 'N/A')}")
        print(f"   Comments: {issue.get('comments', 0)}")
        print(f"   URL: {issue.get('html_url', 'N/A')}")

# Format GitHub pull request results for readable terminal output.

def format_pull_requests_result(result):
    """Format pull request results for terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No pull requests returned.")
        return

    print("\nPull Requests")
    print("==================")

    for index, pull_request in enumerate(data, start=1):
        print(
            f"\n{index}. #{pull_request.get('number', 'N/A')} - "
            f"{pull_request.get('title', 'No title')}"
        )
        print(f"   State: {pull_request.get('state', 'N/A')}")
        print(
            f"   Author: "
            f"{pull_request.get('user', {}).get('login', 'N/A')}"
        )
        print(f"   Comments: {pull_request.get('comments', 0)}")
        print(f"   URL: {pull_request.get('html_url', 'N/A')}")

# Format a single GitHub issue for readable terminal output.

def format_issue_result(result):
    """Format a single issue for terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No issue data returned.")
        return

    if "error" in data:
        print(f"Error: {data['error']}")
        return

    print("\nIssue")
    print("==================")
    print(f"Number: #{data.get('number', 'N/A')}")
    print(f"Title: {data.get('title', 'No title')}")
    print(f"State: {data.get('state', 'N/A')}")
    print(f"Author: {data.get('user', {}).get('login', 'N/A')}")
    print(f"Comments: {data.get('comments', 0)}")
    print(f"URL: {data.get('html_url', 'N/A')}")

# Format a single GitHub pull request for readable terminal output.

def format_pull_request_result(result):
    """Format a single pull request for terminal display."""

    data = get_result_data(result)

    if data is None:
        print("No pull request data returned.")
        return

    print("\nPull Request")
    print("==================")
    print(f"Number: #{data.get('number', 'N/A')}")
    print(f"Title: {data.get('title', 'No title')}")
    print(f"State: {data.get('state', 'N/A')}")
    print(f"Author: {data.get('user', {}).get('login', 'N/A')}")
    print(f"Comments: {data.get('comments', 0)}")
    print(f"URL: {data.get('html_url', 'N/A')}")

def get_integer_input(prompt):
    """Read a valid positive integer from the user."""

    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if number < 1:
            print("Please enter a number greater than 0.")
            continue

        return number

async def interactive_menu(session):
    """Display the GitHub Assistant menu and handle user choice."""

    while True:
        print("\n================================")
        print("     GitHub MCP Assistant")
        print("================================")
        print("1. Get repository")
        print("2. Search repositories")
        print("3. List issues")
        print("4. List pull requests")
        print("5. Get issue")
        print("6. Get pull request")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            owner = input("Owner: ").strip()
            repo = input("Repository: ").strip()

            result = await call_tool(
                session, # session = the current MCP client session.
                "get_repo",{
                    "owner": owner,
                    "repo": repo
                },
            )

            format_repository_result(result)

        elif choice == "2":
            query = input("Search query:").strip()
            limit = get_integer_input("Limit: ")
            page = get_integer_input("Page: ")

            result = await call_tool(
                session,
                "search_repositories",{
                    "query":query,
                    "limit":limit,
                    "page":page,
                },
            )

            format_search_results(result)

        elif choice == "3":
            owner = input("Owner:").strip()
            repo = input("Repository: ").strip()
            limit = int(input("Limit: ").strip())
            page = int(input("Page: ").strip())

            result = await call_tool(
                session,
                "list_issues",
                {
                    "owner": owner,
                    "repo": repo,
                    "limit": limit,
                    "page": page,
                },
            )

            format_issues_result(result)

        elif choice == "4":
            owner = input("Owner: ").strip()
            repo = input("Repository: ").strip()
            limit = int(input("Limit: ").strip())
            page = int(input("Page: ").strip())

            result = await call_tool(
                session,
                "list_pull_requests",
                {
                    "owner": owner,
                    "repo": repo,
                    "limit": limit,
                    "page": page,
                },
            )

            format_pull_requests_result(result)

        elif choice == '5':
            owner = input("Owner: ").strip()
            repo = input("Repository: ").strip()
            issue_number = get_integer_input("Issue number: ")

            result = await call_tool(
                session,
                "get_issue",
                {
                    "owner": owner,
                    "repo": repo,
                    "issue_number": issue_number,
                },
            )

            format_issue_result(result)

        elif choice == "6":
            owner = input("Owner: ").strip()
            repo = input("Repository: ").strip()
            pull_number = get_integer_input("Issue number: ")

            result = await call_tool(
                session,
                "get_pull_request",
                {
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pull_number,
                },
            )

            format_pull_request_result(result)

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please choose 1-7.")
            
               

if __name__ == "__main__":
    asyncio.run(main()) 