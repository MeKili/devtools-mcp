"""Tests for the pure tool functions (deterministic, offline)."""

from devtools_mcp.tools import (
    from_base64,
    sha256_hex,
    to_base64,
    url_decode,
    url_encode,
    word_count,
)


def test_word_count() -> None:
    assert word_count("hello world  foo") == 3
    assert word_count("") == 0


def test_sha256_hex_known_value() -> None:
    # Known SHA-256 digest of the string "abc".
    assert sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_base64_roundtrip() -> None:
    assert to_base64("abc") == "YWJj"
    assert from_base64(to_base64("héllo")) == "héllo"


def test_url_encode() -> None:
    assert url_encode("hello world") == "hello%20world"
    assert url_encode("foo&bar=baz") == "foo%26bar%3Dbaz"
    assert url_encode("") == ""


def test_url_decode() -> None:
    assert url_decode("hello%20world") == "hello world"
    assert url_decode("foo%26bar%3Dbaz") == "foo&bar=baz"
    assert url_decode("") == ""


def test_url_encode_decode_roundtrip() -> None:
    text = "special chars: !@#$%^&*()"
    assert url_decode(url_encode(text)) == text
