"""devtools-mcp — a custom Model Context Protocol server exposing developer tools.

``tools`` holds the pure, framework-free functions; ``server`` exposes them over
MCP (FastMCP, stdio transport). Keeping the logic in ``tools`` means it can be
unit-tested without running the protocol.
"""

__version__ = "0.1.0"
