"""A custom Model Context Protocol (MCP) server exposing developer tools.

Run over stdio with ``python -m devtools_mcp.server`` (or the ``devtools-mcp``
console script). Each tool is a thin wrapper around a pure function in ``tools``.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from devtools_mcp import tools

mcp = FastMCP("devtools")


@mcp.tool()
def char_count(text: str) -> int:
    """Count the number of characters in ``text`` (including spaces and newlines)."""
    return tools.char_count(text)


@mcp.tool()
def word_count(text: str) -> int:
    """Count the whitespace-separated words in ``text``."""
    return tools.word_count(text)


@mcp.tool()
def line_count(text: str) -> int:
    """Count the number of lines in ``text``."""
    return tools.line_count(text)


@mcp.tool()
def md5_hex(text: str) -> str:
    """Return the hex MD5 digest of ``text``."""
    return tools.md5_hex(text)


@mcp.tool()
def sha1_hex(text: str) -> str:
    """Return the hex SHA-1 digest of ``text``."""
    return tools.sha1_hex(text)


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


@mcp.tool()
def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    return tools.slugify(text)


@mcp.tool()
def uuid4_str() -> str:
    """Generate a random UUID4 string."""
    return tools.uuid4_str()


@mcp.tool()
def text_to_hex(text: str) -> str:
    """Convert text (UTF-8) to hexadecimal representation."""
    return tools.text_to_hex(text)


@mcp.tool()
def hex_to_text(hex_str: str) -> str:
    """Convert hexadecimal string back to UTF-8 text."""
    return tools.hex_to_text(hex_str)


@mcp.tool()
def to_snake_case(text: str) -> str:
    """Convert text to snake_case (lowercase with underscores)."""
    return tools.to_snake_case(text)


@mcp.tool()
def to_camel_case(text: str) -> str:
    """Convert text to camelCase (lowercase first, uppercase after separators)."""
    return tools.to_camel_case(text)


@mcp.tool()
def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case (lowercase with hyphens)."""
    return tools.to_kebab_case(text)


@mcp.tool()
def regex_search(text: str, pattern: str) -> list[tools.RegexMatch]:
    """Search for all regex matches in text.

    Returns a list of matches with position information (match, start, end).
    """
    return tools.regex_search(text, pattern)


@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse a string character by character."""
    return tools.reverse_string(text)


@mcp.tool()
def html_escape(text: str) -> str:
    """Escape HTML special characters (& < > \" ')."""
    return tools.html_escape(text)


@mcp.tool()
def html_unescape(text: str) -> str:
    """Unescape HTML entities back to their character equivalents."""
    return tools.html_unescape(text)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
