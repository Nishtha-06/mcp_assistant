## GitHub Client Test: Verifies that the GitHub client can fetch repository, issue, and pull request data.
from server.github_client import GitHubClient

def main():
    client = GitHubClient()

    repository = client.get_repository(
        "Nishtha-06",
        "mcp_assistant",
    )

    print("Repository: ",repository["full_name"])
    print("Description: ",repository["description"])
    print("Stars: ",repository["stargazers_count"])

    issues = client.list_issue(
        "Nishtha-06",
        "mcp_assistant",
    )
    print("\nOpen Issues:")
    for issue in issues:
        print(issue["number"],issue["title"])


    pull_request = client.list_pull_requests(
        "Nishtha-06",
        "mcp_assistant",
    )

    print("Pull requests: ")
    for req in pull_request:
        print(req["number"],req["title"])

if __name__ == "__main__":
    main()