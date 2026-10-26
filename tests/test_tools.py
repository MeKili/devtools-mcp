"""Tests for the pure tool functions (deterministic, offline)."""

import re

from devtools_mcp.tools import (
    char_count,
    count_substring,
    dedent,
    from_base32,
    from_base64,
    hex_to_text,
    html_escape,
    html_unescape,
    join_strings,
    json_minify,
    json_pretty_print,
    line_count,
    lowercase,
    ltrim_string,
    md5_hex,
    regex_search,
    reverse_string,
    rtrim_string,
    sha1_hex,
    sha256_hex,
    slugify,
    sort_lines,
    split_string,
    string_replace,
    text_to_hex,
    to_base32,
    to_base64,
    to_camel_case,
    to_kebab_case,
    to_snake_case,
    trim_string,
    uppercase,
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


def test_base32_encode() -> None:
    assert to_base32("abc") == "MFRGG==="
    assert to_base32("hello") == "NBSWY3DP"
    assert to_base32("") == ""


def test_base32_decode() -> None:
    assert from_base32("MFRGG===") == "abc"
    assert from_base32("NBSWY3DP") == "hello"
    assert from_base32("") == ""


def test_base32_roundtrip() -> None:
    assert to_base32("abc") == "MFRGG==="
    assert from_base32(to_base32("héllo")) == "héllo"
    text = "The quick brown fox"
    assert from_base32(to_base32(text)) == text


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


def test_html_escape_basic() -> None:
    assert html_escape("<div>") == "&lt;div&gt;"
    assert html_escape("a & b") == "a &amp; b"
    assert html_escape('hello "world"') == "hello &quot;world&quot;"
    assert html_escape("it's") == "it&#x27;s"


def test_html_escape_no_special_chars() -> None:
    assert html_escape("hello") == "hello"
    assert html_escape("123") == "123"


def test_html_escape_multiple() -> None:
    assert (
        html_escape("<script>alert('xss')</script>")
        == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
    )


def test_html_unescape_basic() -> None:
    assert html_unescape("&lt;div&gt;") == "<div>"
    assert html_unescape("a &amp; b") == "a & b"
    assert html_unescape("&quot;hello&quot;") == '"hello"'
    assert html_unescape("&#x27;") == "'"


def test_html_unescape_numeric_entities() -> None:
    assert html_unescape("&#169;") == "©"
    assert html_unescape("&#8364;") == "€"


def test_html_unescape_no_entities() -> None:
    assert html_unescape("hello") == "hello"
    assert html_unescape("123") == "123"


def test_html_escape_unescape_roundtrip() -> None:
    text = '<div class="container">Hello & "World"</div>'
    assert html_unescape(html_escape(text)) == text


def test_dedent_basic() -> None:
    text = """
        hello
        world
    """
    result = dedent(text)
    assert result == "\nhello\nworld\n"


def test_dedent_mixed_indent() -> None:
    text = """
        line1
            line2
        line3
    """
    result = dedent(text)
    assert result == "\nline1\n    line2\nline3\n"


def test_dedent_no_common_indent() -> None:
    text = "hello\n    world"
    result = dedent(text)
    assert result == "hello\n    world"


def test_dedent_single_line() -> None:
    text = "hello"
    assert dedent(text) == "hello"


def test_dedent_empty_string() -> None:
    assert dedent("") == ""


def test_dedent_preserves_relative_indentation() -> None:
    text = """
        if True:
            print("hello")
            print("world")
    """
    result = dedent(text)
    assert "if True:" in result
    assert '    print("hello")' in result


def test_string_replace_all_occurrences() -> None:
    assert string_replace("hello world hello", "hello", "hi") == "hi world hi"
    assert string_replace("aaa", "a", "b") == "bbb"
    assert string_replace("test", "x", "y") == "test"


def test_string_replace_limited_count() -> None:
    assert string_replace("hello world hello", "hello", "hi", count=1) == "hi world hello"
    assert string_replace("aaa", "a", "b", count=2) == "bba"
    assert string_replace("test", "e", "E", count=1) == "tEst"


def test_string_replace_zero_count() -> None:
    assert string_replace("hello", "l", "L", count=0) == "hello"


def test_string_replace_empty_search() -> None:
    result = string_replace("abc", "", "x")
    assert result.count("x") > len("abc")


def test_string_replace_empty_text() -> None:
    assert string_replace("", "test", "replacement") == ""


def test_string_replace_empty_replacement() -> None:
    assert string_replace("hello world", "world", "") == "hello "
    assert string_replace("aaa", "a", "") == ""


def test_uppercase_basic() -> None:
    assert uppercase("hello") == "HELLO"
    assert uppercase("world") == "WORLD"
    assert uppercase("") == ""


def test_uppercase_mixed() -> None:
    assert uppercase("HeLLo WoRLd") == "HELLO WORLD"
    assert uppercase("123abc") == "123ABC"


def test_uppercase_special_chars() -> None:
    assert uppercase("hello@world!") == "HELLO@WORLD!"
    assert uppercase("test-case_name") == "TEST-CASE_NAME"


def test_uppercase_unicode() -> None:
    assert uppercase("café") == "CAFÉ"
    assert uppercase("naïve") == "NAÏVE"


def test_lowercase_basic() -> None:
    assert lowercase("HELLO") == "hello"
    assert lowercase("WORLD") == "world"
    assert lowercase("") == ""


def test_lowercase_mixed() -> None:
    assert lowercase("HeLLo WoRLd") == "hello world"
    assert lowercase("123ABC") == "123abc"


def test_lowercase_special_chars() -> None:
    assert lowercase("HELLO@WORLD!") == "hello@world!"
    assert lowercase("TEST-CASE_NAME") == "test-case_name"


def test_lowercase_unicode() -> None:
    assert lowercase("CAFÉ") == "café"
    assert lowercase("NAÏVE") == "naïve"


def test_uppercase_lowercase_roundtrip() -> None:
    assert lowercase(uppercase("Hello World")) == "hello world"
    assert uppercase(lowercase("Hello World")) == "HELLO WORLD"


def test_trim_string_basic() -> None:
    assert trim_string("  hello  ") == "hello"
    assert trim_string("  world  ") == "world"
    assert trim_string("hello") == "hello"


def test_trim_string_tabs_newlines() -> None:
    assert trim_string("\thello\n") == "hello"
    assert trim_string("\n\tworld\t\n") == "world"
    assert trim_string("\r\ntest\r\n") == "test"


def test_trim_string_empty() -> None:
    assert trim_string("") == ""
    assert trim_string("   ") == ""
    assert trim_string("\t\n") == ""


def test_trim_string_internal_spaces() -> None:
    assert trim_string("  hello world  ") == "hello world"
    assert trim_string("\thello  world\n") == "hello  world"


def test_ltrim_string_basic() -> None:
    assert ltrim_string("  hello") == "hello"
    assert ltrim_string("  world  ") == "world  "
    assert ltrim_string("hello") == "hello"


def test_ltrim_string_various_whitespace() -> None:
    assert ltrim_string("\thello") == "hello"
    assert ltrim_string("\n\nworld") == "world"
    assert ltrim_string(" \t\ntest") == "test"


def test_ltrim_string_empty() -> None:
    assert ltrim_string("") == ""
    assert ltrim_string("   ") == ""
    assert ltrim_string("\t\n") == ""


def test_rtrim_string_basic() -> None:
    assert rtrim_string("hello  ") == "hello"
    assert rtrim_string("  world  ") == "  world"
    assert rtrim_string("hello") == "hello"


def test_rtrim_string_various_whitespace() -> None:
    assert rtrim_string("hello\t") == "hello"
    assert rtrim_string("world\n\n") == "world"
    assert rtrim_string("test \t\n") == "test"


def test_rtrim_string_empty() -> None:
    assert rtrim_string("") == ""
    assert rtrim_string("   ") == ""
    assert rtrim_string("\t\n") == ""


def test_split_string_basic() -> None:
    assert split_string("hello,world,test", ",") == ["hello", "world", "test"]
    assert split_string("a|b|c", "|") == ["a", "b", "c"]
    assert split_string("one two three", " ") == ["one", "two", "three"]


def test_split_string_empty_text() -> None:
    assert split_string("", ",") == [""]
    assert split_string("", "|") == [""]


def test_split_string_no_delimiter() -> None:
    assert split_string("hello", ",") == ["hello"]
    assert split_string("test", "|") == ["test"]


def test_split_string_single_delimiter() -> None:
    assert split_string("hello,world", ",") == ["hello", "world"]
    assert split_string("a|b", "|") == ["a", "b"]


def test_split_string_maxsplit_default() -> None:
    assert split_string("a,b,c,d", ",") == ["a", "b", "c", "d"]
    assert split_string("a,b,c,d", ",", -1) == ["a", "b", "c", "d"]


def test_split_string_maxsplit_limited() -> None:
    assert split_string("a,b,c,d", ",", 1) == ["a", "b,c,d"]
    assert split_string("a,b,c,d", ",", 2) == ["a", "b", "c,d"]
    assert split_string("hello world test more", " ", 2) == ["hello", "world", "test more"]


def test_split_string_maxsplit_zero() -> None:
    assert split_string("a,b,c", ",", 0) == ["a,b,c"]
    assert split_string("hello,world", ",", 0) == ["hello,world"]


def test_split_string_multichar_delimiter() -> None:
    assert split_string("hello::world::test", "::") == ["hello", "world", "test"]
    assert split_string("one---two---three", "---") == ["one", "two", "three"]


def test_split_string_consecutive_delimiters() -> None:
    assert split_string("a,,b", ",") == ["a", "", "b"]
    assert split_string("||test||", "|") == ["", "", "test", "", ""]


def test_split_string_trailing_delimiter() -> None:
    assert split_string("hello,", ",") == ["hello", ""]
    assert split_string("test|", "|") == ["test", ""]


def test_split_string_leading_delimiter() -> None:
    assert split_string(",hello", ",") == ["", "hello"]
    assert split_string("|test", "|") == ["", "test"]


def test_join_strings_basic() -> None:
    assert join_strings(",", ["hello", "world", "test"]) == "hello,world,test"
    assert join_strings("|", ["a", "b", "c"]) == "a|b|c"
    assert join_strings(" ", ["one", "two", "three"]) == "one two three"


def test_join_strings_single_element() -> None:
    assert join_strings(",", ["hello"]) == "hello"
    assert join_strings("|", ["single"]) == "single"


def test_join_strings_empty_list() -> None:
    assert join_strings(",", []) == ""
    assert join_strings("|", []) == ""


def test_join_strings_empty_strings() -> None:
    assert join_strings(",", ["", "", ""]) == ",,"
    assert join_strings("|", ["a", "", "b"]) == "a||b"


def test_join_strings_multichar_separator() -> None:
    assert join_strings("::", ["hello", "world"]) == "hello::world"
    assert join_strings("---", ["one", "two", "three"]) == "one---two---three"


def test_join_strings_split_roundtrip() -> None:
    original = "hello,world,test"
    parts = split_string(original, ",")
    assert join_strings(",", parts) == original


def test_join_strings_split_roundtrip_multichar() -> None:
    original = "a::b::c::d"
    parts = split_string(original, "::")
    assert join_strings("::", parts) == original


def test_join_strings_whitespace_separator() -> None:
    assert join_strings("\n", ["line1", "line2", "line3"]) == "line1\nline2\nline3"
    assert join_strings("\t", ["col1", "col2", "col3"]) == "col1\tcol2\tcol3"


def test_join_strings_empty_separator() -> None:
    assert join_strings("", ["h", "e", "l", "l", "o"]) == "hello"
    assert join_strings("", ["a", "b", "c"]) == "abc"


def test_sort_lines_basic() -> None:
    text = "zebra\napple\nbanana"
    result = sort_lines(text)
    assert result == "apple\nbanana\nzebra"


def test_sort_lines_reverse() -> None:
    text = "apple\nbanana\nzebra"
    result = sort_lines(text, reverse=True)
    assert result == "zebra\nbanana\napple"


def test_sort_lines_empty() -> None:
    assert sort_lines("") == ""


def test_sort_lines_single_line() -> None:
    assert sort_lines("hello") == "hello"


def test_sort_lines_duplicate_lines() -> None:
    text = "dog\ncat\ndog\nbird"
    result = sort_lines(text)
    assert result == "bird\ncat\ndog\ndog"


def test_sort_lines_unique() -> None:
    text = "dog\ncat\ndog\nbird\ncat"
    result = sort_lines(text, unique=True)
    assert result == "bird\ncat\ndog"


def test_sort_lines_unique_reverse() -> None:
    text = "apple\nbanana\napple\ncherry"
    result = sort_lines(text, unique=True, reverse=True)
    assert result == "cherry\nbanana\napple"


def test_sort_lines_numbers_as_strings() -> None:
    text = "3\n1\n2"
    result = sort_lines(text)
    assert result == "1\n2\n3"


def test_sort_lines_case_sensitive() -> None:
    text = "Apple\napple\nBanana\nbanana"
    result = sort_lines(text)
    assert result == "Apple\nBanana\napple\nbanana"


def test_sort_lines_whitespace_preserved() -> None:
    text = "  hello\nworld\n  test"
    result = sort_lines(text)
    assert result == "  hello\n  test\nworld"


def test_sort_lines_with_trailing_newline() -> None:
    text = "zebra\napple\nbanana\n"
    result = sort_lines(text)
    assert result == "apple\nbanana\nzebra"


def test_count_substring_basic() -> None:
    assert count_substring("hello world", "o") == 2
    assert count_substring("hello world", "l") == 3
    assert count_substring("hello world", "world") == 1


def test_count_substring_not_found() -> None:
    assert count_substring("hello", "x") == 0
    assert count_substring("hello world", "test") == 0
    assert count_substring("abc", "xyz") == 0


def test_count_substring_empty_substring() -> None:
    assert count_substring("hello", "") == 0
    assert count_substring("", "") == 0


def test_count_substring_empty_text() -> None:
    assert count_substring("", "a") == 0
    assert count_substring("", "test") == 0


def test_count_substring_single_occurrence() -> None:
    assert count_substring("hello", "hello") == 1
    assert count_substring("test string", "test") == 1


def test_count_substring_multiple_occurrences() -> None:
    assert count_substring("aaaa", "a") == 4
    assert count_substring("abcabcabc", "abc") == 3
    assert count_substring("hello hello hello", "hello") == 3


def test_count_substring_overlapping() -> None:
    # count_substring counts non-overlapping occurrences
    assert count_substring("aaa", "aa") == 1
    assert count_substring("aaaa", "aa") == 2


def test_count_substring_case_sensitive() -> None:
    assert count_substring("Hello HELLO hello", "hello") == 1
    assert count_substring("Hello HELLO hello", "HELLO") == 1
    assert count_substring("Hello HELLO hello", "Hello") == 1


def test_count_substring_multichar() -> None:
    assert count_substring("foo bar foo baz foo", "foo") == 3
    assert count_substring("one::two::three", "::") == 2
    assert count_substring("test---test---test", "---") == 2
