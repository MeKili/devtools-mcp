"""Tests for the pure tool functions (deterministic, offline)."""

from devtools_mcp.tools import (
    from_base64,
    json_minify,
    json_pretty_print,
    sha256_hex,
    slugify,
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


def test_json_minify() -> None:
    input_json = '{"name": "Alice", "age": 30, "items": [1, 2, 3]}'
    minified = json_minify(input_json)
    assert minified == '{"name":"Alice","age":30,"items":[1,2,3]}'
    assert "\n" not in minified
    assert "  " not in minified


def test_json_pretty_print() -> None:
    input_json = '{"name":"Alice","age":30}'
    pretty = json_pretty_print(input_json)
    assert '"name": "Alice"' in pretty
    assert '"age": 30' in pretty
    assert "\n" in pretty


def test_json_minify_pretty_roundtrip() -> None:
    original = {"name": "Bob", "tags": ["a", "b"]}
    import json as stdlib_json

    json_str = stdlib_json.dumps(original)
    minified = json_minify(json_str)
    pretty = json_pretty_print(minified)
    assert stdlib_json.loads(pretty) == original


def test_json_minify_invalid() -> None:
    import pytest

    with pytest.raises(ValueError):
        json_minify("not valid json {")


def test_json_pretty_print_invalid() -> None:
    import pytest

    with pytest.raises(ValueError):
        json_pretty_print("{invalid}")


def test_slugify_basic() -> None:
    assert slugify("Hello World") == "hello-world"
    assert slugify("") == ""
    assert slugify("a") == "a"


def test_slugify_special_chars() -> None:
    assert slugify("foo@bar#baz") == "foobarbaz"
    assert slugify("hello!!!world") == "helloworld"


def test_slugify_spaces_underscores() -> None:
    assert slugify("hello_world test") == "hello-world-test"
    assert slugify("  multiple   spaces  ") == "multiple-spaces"


def test_slugify_accents() -> None:
    assert slugify("café") == "cafe"
    assert slugify("naïve") == "naive"
    assert slugify("Zürich") == "zurich"


def test_slugify_consecutive_hyphens() -> None:
    assert slugify("foo---bar") == "foo-bar"
    assert slugify("hello___world") == "hello-world"


def test_slugify_leading_trailing() -> None:
    assert slugify("---hello-world---") == "hello-world"
    assert slugify("___slug___") == "slug"
    assert slugify("-test-") == "test"
