import os

import base64
import csv
import io
import os
from typing import Any

import matplotlib.pyplot as plt
from fastmcp import FastMCP

mcp = FastMCP()

# The MCP tool can use other functions inside it
def _main_add_tool(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return a + b

def _generate_plot_image(a: int, b: int, total: int) -> str:
    """Create a simple bar plot and return base64 PNG data."""
    labels = ["First", "Second", "Sum"]
    values = [a, b, total]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(labels, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_ylabel("Value")
    ax.set_title("Addition Result")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii")

def _generate_csv_data_uri(a: int, b: int, total: int) -> str:
    """Return CSV content encoded as a data URI for download."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["first_number", "second_number", "sum"])
    writer.writerow([a, b, total])
    encoded = base64.b64encode(buffer.getvalue().encode("utf-8")).decode("ascii")
    return f"data:text/csv;base64,{encoded}"

@mcp.tool()
def add(a: int, b: int) -> list[dict[str, Any]]:
    """
    Add two numbers together
    """
    total = _main_add_tool(a, b)
    plot_data = _generate_plot_image(a, b, total)
    csv_uri = _generate_csv_data_uri(a, b, total)

    return [
        {"type": "text", "text": f"{a} + {b} = {total}"},
        {
            "type": "image",
            "image": {
                "mimeType": "image/png",
                "data": plot_data,
            },
        },
        {
            "type": "resource",
            "resource": {
                "uri": csv_uri,
                "mimeType": "text/csv",
                "name": "addition.csv",
            },
        },
    ]

if __name__ == "__main__":
    # Render provides PORT env var; default to 8000 for local dev
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
    )