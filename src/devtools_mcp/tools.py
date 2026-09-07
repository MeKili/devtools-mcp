"""Pure functions backing the MCP developer tools (no protocol or I/O here)."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import unicodedata
import uuid
from urllib.parse import quote, unquote


def char_count(text: str) -> int:
    """Return the number of characters in ``text`` (including spaces and newlines)."""
    return len(text)


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in ``text``."""
    return len(text.split())


def md5_hex(text: str) -> str:
    """Return the hex MD5 digest of ``text`` (encoded as UTF-8)."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha1_hex(text: str) -> str:
    """Return the hex SHA-1 digest of ``text`` (encoded as UTF-8)."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


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


def json_minify(data: str) -> str:
    """Parse JSON and return a minified (compact, no whitespace) version.

    Raises ValueError if the input is not valid JSON.
    """
    parsed = json.loads(data)
    return json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)


def json_pretty_print(data: str, indent: int = 2) -> str:
    """Parse JSON and return a pretty-printed (indented) version.

    Raises ValueError if the input is not valid JSON.
    """
    parsed = json.loads(data)
    return json.dumps(parsed, indent=indent, ensure_ascii=False)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Converts to lowercase, removes accents, replaces spaces/underscores with
    hyphens, removes special characters, and collapses consecutive hyphens.
    """
    # Normalize unicode and remove accents
    normalized = unicodedata.normalize("NFKD", text)
    text_without_accents = normalized.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    text_lower = text_without_accents.lower()

    # Replace spaces and underscores with hyphens
    text_hyphens = re.sub(r"[\s_]+", "-", text_lower)

    # Remove any character that's not alphanumeric or hyphen
    text_clean = re.sub(r"[^a-z0-9-]", "", text_hyphens)

    # Collapse consecutive hyphens
    text_collapsed = re.sub(r"-+", "-", text_clean)

    # Strip leading/trailing hyphens
    return text_collapsed.strip("-")


def uuid4_str() -> str:
    """Generate a random UUID4 string."""
    return str(uuid.uuid4())


def text_to_hex(text: str) -> str:
    """Convert text (UTF-8) to hexadecimal representation."""
    return text.encode("utf-8").hex()


def hex_to_text(hex_str: str) -> str:
    """Convert hexadecimal string back to UTF-8 text.

    Raises ValueError if the input is not a valid hex string.
    """
    return bytes.fromhex(hex_str).decode("utf-8")


def to_snake_case(text: str) -> str:
    """Convert text to snake_case (lowercase with underscores).

    Handles camelCase, kebab-case, space-separated, and mixed input.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    s3 = re.sub(r"[-\s]+", "_", s2)
    s4 = re.sub(r"_+", "_", s3)
    return s4.lower()


def to_camel_case(text: str) -> str:
    """Convert text to camelCase (lowercase first, uppercase after separators).

    Handles snake_case, kebab-case, space-separated, and mixed input.
    """
    components = re.split(r"[-_\s]+", text)
    if not components:
        return ""
    return components[0].lower() + "".join(x.title() for x in components[1:])


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case (lowercase with hyphens).

    Handles camelCase, snake_case, space-separated, and mixed input.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", text)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1)
    s3 = re.sub(r"[_\s]+", "-", s2)
    return s3.lower()
