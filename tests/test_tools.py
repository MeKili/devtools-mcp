"""Tests for the pure tool functions (deterministic, offline)."""

from devtools_mcp.tools import from_base64, sha256_hex, to_base64, word_count


def test_word_count() -> None:
    assert word_count("hello world  foo") == 3
    assert word_count("") == 0


def test_sha256_hex_known_value() -> None:
    # Known SHA-256 digest of the string "abc".
    assert sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_base64_roundtrip() -> None:
    assert to_base64("abc") == "YWJj"
    assert from_base64(to_base64("héllo")) == "héllo"
