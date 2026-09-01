# GitHub Error Tests: Verifies that the GitHub client safely handles API and network errors.

import httpx
from server.github_client import GitHubAPIError,GitHubClient

def test_invalid_repo():
    """Test that an empty repo name is rejected."""

    client = GitHubClient()

    try:
        # We expect this invalid input to raise a ValueError.
        client.get_repository("Nishtha-06","")

        # If no error occurs, the invalid repository was accepted, so the test fails.
        print("FAIL: Empty repository was accepted.")

    except ValueError as error:
        # ValueError is expected here because an empty repository name is invalid.
        # Getting the expected error means the validation worked correctly.
        print("PASS: Invalid repository rejected.")
        print("Error: ",error)

def test_invalid_owner():
    """Test that an empty repository owner is rejected."""

    client = GitHubClient()

    try:
        client.get_repository("","mcp_assistant")
        print("FAIL: Empty owner was accepted.")

    except ValueError as error:
        print("PASS: Invalid owner rejected.")
        print("Error:", error)

def test_401_error():
    """Test that 401 response is handled correctly."""

    client = GitHubClient()
    response = httpx.Response(status_code=401)

    try:
        client._handle_response_error(response)
        print("FAIL: 401 error was not handled.")
    except GitHubAPIError as error:
        print("PASS: 401 error handled correctly.")
        print("Error:", error)

def test_403_error():
    """Test that 403 response is handled correctly."""

    client = GitHubClient()
    response = httpx.Response(status_code=403)

    try:
        client._handle_response_error(response)
        print("FAIL: 403 error was not handled.")
    except GitHubAPIError as error:
        print("PASS: 403 error handled correctly.")
        print("Error:", error)

def test_404_error():
    """Test that 404 response is handled correctly."""

    client = GitHubClient()
    response = httpx.Response(status_code=404)

    try:
        client._handle_response_error(response)
        print("FAIL: 404 error was not handled.")
    except GitHubAPIError as error:
        print("PASS: 404 error handled correctly.")
        print("Error:", error)

def test_500_error():
    """Test that 500 response is handled correctly."""

    client = GitHubClient()
    response = httpx.Response(status_code=500)

    try:
        client._handle_response_error(response)
        print("FAIL: 500 error was not handled.")
    except GitHubAPIError as error:
        print("PASS: 500 error handled correctly.")
        print("Error:", error)

def test_timeout_error():
    """Test that timeout error is handled correctly."""

    client = GitHubClient()

    try:
        # Simulate a timeout by calling a non-routable IP address.
        client._request("GET", "http://10.255.255.1")
        print("FAIL: Timeout error was not handled.")

    except GitHubAPIError as error:
        print("PASS: Timeout error handled correctly.")
        print("Error:", error)

def test_network_error():
    """Test that network error is handled correctly."""

    client = GitHubClient()

    try:
        # Simulate a network error by calling an invalid URL.
        client._request("GET", "http://127.0.0.1:1")
        print("FAIL: Network error was not handled.")

    except GitHubAPIError as error:
        print("PASS: Network error handled correctly.")
        print("Error:", error)

if __name__ == "__main__":
    test_invalid_repo()
    test_invalid_owner()

    test_401_error()
    test_403_error()
    test_404_error()
    test_500_error()

    test_timeout_error()
    test_network_error()