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


@mcp.tool()
def url_encode(text: str) -> str:
    """URL-encode text (percent-encoding special characters)."""
    return tools.url_encode(text)


@mcp.tool()
def url_decode(text: str) -> str:
    """URL-decode a percent-encoded string."""
    return tools.url_decode(text)


@mcp.tool()
def json_minify(data: str) -> str:
    """Minify JSON (remove all unnecessary whitespace)."""
    return tools.json_minify(data)


@mcp.tool()
def json_pretty_print(data: str, indent: int = 2) -> str:
    """Pretty-print JSON with indentation (default 2 spaces)."""
    return tools.json_pretty_print(data, indent=indent)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
