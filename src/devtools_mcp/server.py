"""A custom Model Context Protocol (MCP) server exposing developer tools.

Run over stdio with ``python -m devtools_mcp.server`` (or the ``devtools-mcp``
console script). Each tool is a thin wrapper around a pure function in ``tools``.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from devtools_mcp import tools

mcp = FastMCP("devtools")


@mcp.tool()
def word_count(text: str) -> int:
    """Count the whitespace-separated words in ``text``."""
    return tools.word_count(text)


@mcp.tool()
def sha256_hex(text: str) -> str:
    """Return the hex SHA-256 digest of ``text``."""
    return tools.sha256_hex(text)


@mcp.tool()
def to_base64(text: str) -> str:
    """Base64-encode ``text``."""
    return tools.to_base64(text)


@mcp.tool()
def from_base64(data: str) -> str:
    """Decode a base64 string back to text."""
    return tools.from_base64(data)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
