from greas3.local import has_expected_hash


def test_has_expected_hash__chunk() -> None:
    expect = b"eh,\xcf\xcbI+\xa2\x9d\x19\x0bV\xb8a\x06\x0c\x05r[\xfe#l\xccF\x87\xedR\x13\xee\xbf\xe7^"  # noqa: E501
    assert has_expected_hash("README.md", expect, offset=10, length=20)


def test_has_expected_hash__entire() -> None:
    expect = b"\t\xf19\x17F \xd3\xee\xbfNLG\xcc2\xe5\xcb\x17d\xbf\xe0\xb0\xcf\xc7\x8b;\xc3\xf0\x17\x92\x15\xc4\xd2"  # noqa: E501
    assert has_expected_hash("README.md", expect)
