import os

from fastmcp import FastMCP

mcp = FastMCP()

# The MCP tool can use other functions inside it
def _main_add_tool(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return a + b

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return _main_add_tool(a, b)

if __name__ == "__main__":
    # Render provides PORT env var; default to 8000 for local dev
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
    )