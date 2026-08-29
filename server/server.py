from mcp.server.fastmcp import FastMCP #FastMCPServer is a convenient way to create an MCP server in Python.

mcp = FastMCP("GitHub MCP Assistant") # Create an instance of the FastMCPServer class.  

@mcp.tool() # the function immediately below this decorator will be a tool in the MCP server.
def hello(name: str) -> str: 
    """Return a greeting message."""
    return f"Hello, {name}!" 

if __name__ == "__main__": # This block ensures that the server runs only when this script is executed directly(python server.py), not when imported as a module.
    mcp.run()

