"""Pure functions backing the MCP developer tools (no protocol or I/O here)."""

from __future__ import annotations

import base64
import hashlib
from urllib.parse import quote, unquote


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in ``text``."""
    return len(text.split())


def sha256_hex(text: str) -> str:
    """Return the hex SHA-256 digest of ``text`` (encoded as UTF-8)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def to_base64(text: str) -> str:
    """Base64-encode ``text`` (UTF-8) and return an ASCII string."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def from_base64(data: str) -> str:
    """Decode a base64 ``data`` string back to UTF-8 text."""
    return base64.b64decode(data.encode("ascii")).decode("utf-8")


def url_encode(text: str) -> str:
    """URL-encode ``text`` (percent-encoding special characters)."""
    return quote(text, safe="")


def url_decode(text: str) -> str:
    """URL-decode a percent-encoded ``text`` string."""
    return unquote(text)
