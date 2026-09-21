"""Tests for the pure tool functions (deterministic, offline)."""

import re

from devtools_mcp.tools import (
    char_count,
    from_base64,
    hex_to_text,
    json_minify,
    json_pretty_print,
    line_count,
    md5_hex,
    regex_search,
    reverse_string,
    sha1_hex,
    sha256_hex,
    slugify,
    text_to_hex,
    to_base64,
    to_camel_case,
    to_kebab_case,
    to_snake_case,
    url_decode,
    url_encode,
    uuid4_str,
    word_count,
)


def test_char_count() -> None:
    assert char_count("hello") == 5
    assert char_count("hello world") == 11
    assert char_count("") == 0
    assert char_count("\n\n") == 2
    assert char_count("café") == 4


def test_word_count() -> None:
    assert word_count("hello world  foo") == 3
    assert word_count("") == 0


def test_line_count_single_line() -> None:
    assert line_count("hello") == 1
    assert line_count("hello world") == 1


def test_line_count_multiple_lines() -> None:
    assert line_count("hello\nworld") == 2
    assert line_count("line1\nline2\nline3") == 3


def test_line_count_empty() -> None:
    assert line_count("") == 0


def test_line_count_trailing_newline() -> None:
    assert line_count("hello\n") == 1
    assert line_count("hello\nworld\n") == 2


def test_line_count_multiple_newlines() -> None:
    assert line_count("hello\n\nworld") == 3
    assert line_count("\n\n\n") == 3


def test_line_count_with_carriage_return() -> None:
    assert line_count("hello\r\nworld") == 2
    assert line_count("line1\r\nline2\r\nline3") == 3


def test_md5_hex_known_value() -> None:
    # Known MD5 digest of the string "abc".
    assert md5_hex("abc") == "900150983cd24fb0d6963f7d28e17f72"


def test_sha1_hex_known_value() -> None:
    # Known SHA-1 digest of the string "abc".
    assert sha1_hex("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d"


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


def test_uuid4_str_format() -> None:
    import uuid as stdlib_uuid

    result = uuid4_str()
    assert isinstance(result, str)
    parsed = stdlib_uuid.UUID(result)
    assert parsed.version == 4


def test_uuid4_str_uniqueness() -> None:
    uuid1 = uuid4_str()
    uuid2 = uuid4_str()
    assert uuid1 != uuid2


def test_text_to_hex_basic() -> None:
    assert text_to_hex("abc") == "616263"
    assert text_to_hex("hello") == "68656c6c6f"
    assert text_to_hex("") == ""


def test_text_to_hex_utf8() -> None:
    assert text_to_hex("café") == "636166c3a9"
    assert text_to_hex("🎉") == "f09f8e89"


def test_hex_to_text_basic() -> None:
    assert hex_to_text("616263") == "abc"
    assert hex_to_text("68656c6c6f") == "hello"
    assert hex_to_text("") == ""


def test_hex_to_text_utf8() -> None:
    assert hex_to_text("636166c3a9") == "café"
    assert hex_to_text("f09f8e89") == "🎉"


def test_text_hex_roundtrip() -> None:
    text = "hello world 123!@#"
    assert hex_to_text(text_to_hex(text)) == text


def test_hex_to_text_utf8_roundtrip() -> None:
    text = "café naïve Zürich 🎉"
    assert hex_to_text(text_to_hex(text)) == text


def test_hex_to_text_invalid() -> None:
    import pytest

    with pytest.raises(ValueError):
        hex_to_text("not_hex_at_all")


def test_to_snake_case_camel() -> None:
    assert to_snake_case("helloWorld") == "hello_world"
    assert to_snake_case("HelloWorld") == "hello_world"
    assert to_snake_case("myVariableName") == "my_variable_name"


def test_to_snake_case_kebab() -> None:
    assert to_snake_case("hello-world") == "hello_world"
    assert to_snake_case("my-variable-name") == "my_variable_name"


def test_to_snake_case_spaces() -> None:
    assert to_snake_case("hello world") == "hello_world"
    assert to_snake_case("my variable name") == "my_variable_name"


def test_to_snake_case_mixed() -> None:
    assert to_snake_case("HelloWorld-Test") == "hello_world_test"
    assert to_snake_case("myVar_name-test") == "my_var_name_test"


def test_to_camel_case_snake() -> None:
    assert to_camel_case("hello_world") == "helloWorld"
    assert to_camel_case("my_variable_name") == "myVariableName"


def test_to_camel_case_kebab() -> None:
    assert to_camel_case("hello-world") == "helloWorld"
    assert to_camel_case("my-variable-name") == "myVariableName"


def test_to_camel_case_spaces() -> None:
    assert to_camel_case("hello world") == "helloWorld"
    assert to_camel_case("my variable name") == "myVariableName"


def test_to_camel_case_mixed() -> None:
    assert to_camel_case("hello_world-test") == "helloWorldTest"
    assert to_camel_case("my-var_name test") == "myVarNameTest"


def test_to_kebab_case_snake() -> None:
    assert to_kebab_case("hello_world") == "hello-world"
    assert to_kebab_case("my_variable_name") == "my-variable-name"


def test_to_kebab_case_camel() -> None:
    assert to_kebab_case("helloWorld") == "hello-world"
    assert to_kebab_case("myVariableName") == "my-variable-name"


def test_to_kebab_case_spaces() -> None:
    assert to_kebab_case("hello world") == "hello-world"
    assert to_kebab_case("my variable name") == "my-variable-name"


def test_to_kebab_case_mixed() -> None:
    assert to_kebab_case("hello_world-test") == "hello-world-test"
    assert to_kebab_case("myVar_name test") == "my-var-name-test"


def test_regex_search_basic() -> None:
    result = regex_search("hello world", r"\w+")
    assert len(result) == 2
    assert result[0]["match"] == "hello"
    assert result[0]["start"] == 0
    assert result[0]["end"] == 5
    assert result[1]["match"] == "world"
    assert result[1]["start"] == 6
    assert result[1]["end"] == 11


def test_regex_search_no_matches() -> None:
    result = regex_search("hello", r"\d+")
    assert result == []


def test_regex_search_digits() -> None:
    result = regex_search("a1b2c3", r"\d")
    assert len(result) == 3
    assert result[0]["match"] == "1"
    assert result[1]["match"] == "2"
    assert result[2]["match"] == "3"


def test_regex_search_groups() -> None:
    result = regex_search("test@example.com", r"[a-zA-Z0-9]+@[a-zA-Z0-9.]+")
    assert len(result) == 1
    assert result[0]["match"] == "test@example.com"


def test_regex_search_multiline() -> None:
    text = "line1\nline2\nline3"
    result = regex_search(text, r"line\d")
    assert len(result) == 3
    assert all(r["match"].startswith("line") for r in result)


def test_regex_search_case_insensitive() -> None:
    result = regex_search("Hello HELLO hello", r"(?i)hello")
    assert len(result) == 3
    assert all(r["match"].lower() == "hello" for r in result)


def test_regex_search_invalid_pattern() -> None:
    import pytest

    with pytest.raises(re.error):
        regex_search("test", r"[invalid")


def test_reverse_string_basic() -> None:
    assert reverse_string("hello") == "olleh"
    assert reverse_string("abc") == "cba"
    assert reverse_string("") == ""


def test_reverse_string_special_chars() -> None:
    assert reverse_string("hello!") == "!olleh"
    assert reverse_string("123 abc") == "cba 321"


def test_reverse_string_unicode() -> None:
    assert reverse_string("café") == "éfac"
    assert reverse_string("🎉hello") == "olleh🎉"


def test_reverse_string_single_char() -> None:
    assert reverse_string("a") == "a"
    assert reverse_string("🎉") == "🎉"


def test_reverse_string_palindrome() -> None:
    palindrome = "racecar"
    assert reverse_string(palindrome) == palindrome
