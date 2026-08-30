                START
                  │
                  ▼
             server.py
                  │
                  │ import
                  ▼
          github_client.py
                  │
                  │ loaded
                  ▼
             server.py
                  │
                  │ create tools
                  ▼
             mcp.run()
                  │
                  │ WAIT
                  ▼
             MCP CLIENT
                  │
                  │ request
                  ▼
             MCP SERVER
                  │
                  ▼
        get_repository TOOL
                  │
                  │ github.get_repository()
                  ▼
          GitHubClient method
                  │
                  │ httpx.get()
                  ▼
             GitHub API
                  │
                  ▼
               GitHub