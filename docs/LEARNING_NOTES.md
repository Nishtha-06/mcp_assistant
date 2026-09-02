# MCP Client — Learning Notes

## 1. What is the MCP Client?

The MCP Client connects to the GitHub MCP Server and allows the client to:

* Connect to the MCP server.
* Initialize an MCP session.
* Discover available MCP tools.
* Call MCP tools.
* Receive results from the MCP server.

The basic communication flow is:

```text
MCP Client
    │
    │  stdio
    ▼
MCP Server
    │
    ▼
GitHub Client
    │
    ▼
GitHub REST API
```

The MCP Client is therefore the part that communicates with the MCP Server on behalf of the user or another application.

---

# 2. `asyncio`

```python
import asyncio
```

`asyncio` is Python's library for working with asynchronous programming.

Instead of blocking everything while waiting for an operation to finish, asynchronous programming allows the program to wait efficiently.

For example, communication with an MCP server involves waiting for messages and responses.

Because these operations are asynchronous, we use:

```python
async def
```

and:

```python
await
```

---

# 3. `ClientSession`

```python
from mcp import ClientSession
```

`ClientSession` represents the conversation/session between the MCP Client and MCP Server.

It is responsible for communication after the connection has been established.

Conceptually:

```text
MCP Client
    │
    │
ClientSession
    │
    ▼
MCP Server
```

The session allows the client to perform operations such as:

```python
await session.initialize()
```

```python
await session.list_tools()
```

and eventually:

```python
await session.call_tool(...)
```

---

# 4. `StdioServerParameters`

```python
from mcp import StdioServerParameters
```

`StdioServerParameters` is used to configure how the MCP Client starts and communicates with the MCP Server.

In our project:

```python
server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "-m", "server.server"],
)
```

This tells the MCP Client how to start our MCP Server.

### `command`

```python
command="uv"
```

The command used to start the server is `uv`.

### `args`

```python
args=["run", "python", "-m", "server.server"]
```

These are the arguments passed to `uv`.

It is equivalent to running:

```powershell
uv run python -m server.server
```

So the MCP Client is effectively saying:

> Start my MCP Server using this command.

---

# 5. `stdio`

```python
from mcp.client.stdio import stdio_client
```

`stdio` means:

> Standard Input / Standard Output

The MCP Client communicates with the MCP Server through these streams.

The client uses:

```text
write
```

to send messages to the server.

The client uses:

```text
read
```

to receive messages from the server.

Conceptually:

```text
             MCP Client
                 │
          ┌──────┴──────┐
          │             │
        write          read
          │             ▲
          │             │
          ▼             │
             MCP Server
```

---

# 6. `stdio_client()`

```python
async with stdio_client(server_params) as (read, write):
```

`stdio_client()` creates a connection to the MCP Server using standard input/output.

It uses the `server_params` configuration to know how to start the server.

It gives us two communication streams:

```python
read
write
```

### `write`

Used to send messages from the MCP Client to the MCP Server.

### `read`

Used to receive messages from the MCP Server.

---

# 7. Why are there two `async with` statements?

Our code contains:

```python
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
```

This is **not a function inside a function**.

These are nested asynchronous context managers.

The first one:

```python
async with stdio_client(server_params) as (read, write):
```

creates the communication connection.

The second one:

```python
async with ClientSession(read, write) as session:
```

uses those communication streams to create an MCP session.

Think about it in two steps:

```text
Step 1
stdio_client()
     ↓
read + write streams
     ↓
Step 2
ClientSession(read, write)
     ↓
MCP session
```

The nesting makes sure that resources are properly opened and closed.

---

# 8. `ClientSession(read, write)`

```python
async with ClientSession(read, write) as session:
```

The `ClientSession` takes the:

```python
read
write
```

communication channels created by `stdio_client()`.

It then creates an MCP client session.

We store that session in:

```python
session
```

We can then use:

```python
session
```

to communicate with the MCP Server.

For example:

```python
await session.initialize()
```

and:

```python
await session.list_tools()
```

---

# 9. `session.initialize()`

```python
await session.initialize()
```

This initializes the MCP client session.

In simple terms:

> It starts the MCP communication and performs the initialization/handshake between the client and server.

The client and server need to establish that they are ready to communicate before normal MCP operations can happen.

Conceptually:

```text
MCP Client                         MCP Server
    │                                  │
    │──── initialize request ─────────►│
    │                                  │
    │◄──── initialization response ───│
    │                                  │
    │        Connection ready          │
```

The `await` is important because initialization is asynchronous.

The client sends the initialization request and waits for the server's response.

---

# 10. Why do we use `await`?

For example:

```python
await session.initialize()
```

and:

```python
result = await session.list_tools()
```

`await` means:

> Wait for this asynchronous operation to finish before continuing.

MCP communication involves sending messages and waiting for responses.

Therefore, these operations are asynchronous.

Without `await`, we would not properly wait for the operation's result.

---

# 11. `session.list_tools()`

```python
result = await session.list_tools()
```

This asks the MCP Server:

> What tools do you provide?

The server returns information about the tools registered using:

```python
@mcp.tool()
```

For example, our server currently exposes tools such as:

```text
hello
get_repo
search_repositories
list_issues
list_pull_requests
get_issue
get_pull_request
```

The result is stored in:

```python
result
```

---

# 12. `result.tools`

```python
for tool in result.tools:
```

`result.tools` contains the tools returned by the MCP Server.

We loop through them one at a time:

```python
for tool in result.tools:
```

Each `tool` represents one MCP tool.

---

# 13. `tool.name`

```python
tool.name
```

This gives us the name of the MCP tool.

For example:

```text
hello
get_repo
search_repositories
list_issues
```

---

# 14. `tool.description`

```python
tool.description
```

This gives us the description of the tool.

The description comes from the tool's Python docstring.

For example:

```python
@mcp.tool()
def get_repo(owner: str, repo: str) -> dict:
    """Get information about a GitHub repository."""
```

The MCP client can discover that description.

Therefore the client can display:

```text
get_repo: Get information about a GitHub repository.
```

---

# 15. Displaying Available Tools

Our code:

```python
print("\nAvailable tools on the MCP server:")

for tool in result.tools:
    print(f" - {tool.name}: {tool.description}")
```

produces something like:

```text
Available tools on the MCP server:
 - hello: Return a greeting message.
 - get_repo: Get information about a GitHub repository
 - search_repositories: Search GitHub repositories.
 - list_issues: List open issues from a GitHub repository.
 - list_pull_requests: List open pull requests from a GitHub repository.
 - get_issue: Get a specific issue from github repo
 - get_pull_request: Get a specific pull request from a GitHub repository.
```

This proves that the MCP Client successfully connected to the MCP Server and discovered its tools.

---

# 16. `async def main()`

```python
async def main():
```

`main()` is an asynchronous function.

We use `async def` because it contains asynchronous operations such as:

```python
await session.initialize()
```

and:

```python
await session.list_tools()
```

---

# 17. Running the asynchronous `main()`

At the bottom of the file:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

`asyncio.run(main())` starts the asynchronous event loop and executes `main()`.

Without this, Python would not automatically execute the asynchronous function.

The flow is:

```text
Python starts program
       ↓
__name__ == "__main__"
       ↓
asyncio.run(main())
       ↓
main()
       ↓
connect to MCP server
       ↓
initialize session
       ↓
discover tools
       ↓
display tools
```

---

# 18. Complete MCP Client Flow

The complete process in our current client is:

```text
1. Start Python program
          ↓
2. asyncio.run(main())
          ↓
3. Create stdio connection
          ↓
4. Start MCP Server
          ↓
5. Get read/write streams
          ↓
6. Create ClientSession
          ↓
7. Initialize MCP session
          ↓
8. Ask server for available tools
          ↓
9. Receive tool information
          ↓
10. Display tool names and descriptions
```

---

# 19. Current Client Capability

At this stage, our MCP Client can:

* Start the MCP Server.
* Connect through stdio.
* Establish an MCP session.
* Perform MCP initialization.
* Discover available tools.
* Display tool names.
* Display tool descriptions.

Example:

```text
MCP Client
    │
    │ start server
    ▼
MCP Server
    │
    │ initialize
    ▼
MCP Session
    │
    │ list_tools()
    ▼
Available Tools
```

---

# 20. Important Difference: Discovering vs Calling Tools

Currently:

```python
await session.list_tools()
```

only **discovers** the tools.

It does not execute them.

For example, discovering:

```text
search_repositories
```

does not actually perform a GitHub search.

The next major capability is:

```python
await session.call_tool(...)
```

which will allow the MCP Client to actually call a tool on the MCP Server.

The future flow will be:

```text
MCP Client
    │
    │ call_tool("search_repositories")
    ▼
MCP Server
    │
    ▼
search_repositories()
    │
    ▼
GitHubClient
    │
    ▼
GitHub API
    │
    ▼
Search Results
    │
    ▼
MCP Client
```

This is an important next step because it changes the client from a tool-discovery client into a client that can actually **use the MCP tools**.

---

# 21. Key Concepts to Remember

| Concept                 | Meaning                                     |
| ----------------------- | ------------------------------------------- |
| `asyncio`               | Python library for asynchronous programming |
| `async def`             | Defines an asynchronous function            |
| `await`                 | Waits for an asynchronous operation         |
| `StdioServerParameters` | Configures how the MCP server is started    |
| `stdio`                 | Standard input/output communication         |
| `stdio_client()`        | Creates the stdio connection                |
| `read`                  | Receives messages from the server           |
| `write`                 | Sends messages to the server                |
| `ClientSession`         | Represents the MCP client-server session    |
| `initialize()`          | Performs MCP initialization/handshake       |
| `list_tools()`          | Discovers tools provided by the MCP server  |
| `result.tools`          | Contains the discovered tools               |
| `tool.name`             | Name of an MCP tool                         |
| `tool.description`      | Description of an MCP tool                  |
| `call_tool()`           | Used to execute an MCP tool                 |

---

# 22. Current Project Architecture

```text
                    ┌─────────────────────┐
                    │     MCP Client      │
                    │   client/mcp_client │
                    └──────────┬──────────┘
                               │
                              stdio
                               │
                               ▼
                    ┌─────────────────────┐
                    │     MCP Server      │
                    │    server/server.py │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    GitHub Client    │
                    │ server/github_client│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     GitHub API      │
                    └─────────────────────┘
```

The MCP Client does not directly communicate with the GitHub API.

Instead:

```text
MCP Client
    ↓
MCP Server
    ↓
GitHubClient
    ↓
GitHub API
```

This separation makes the project easier to maintain and demonstrates the MCP architecture clearly.
