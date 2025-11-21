from fastmcp import FastMCP

mcp = FastMCP()

# The MCP tool can use other functions inside it
def main_add_tool(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return a + b

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return main_add_tool(a, b)

if __name__ == "__main__":
    mcp.run(transport="http",
    port=8000)