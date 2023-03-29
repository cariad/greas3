from typing import Optional, Tuple

from pytest import mark

from greas3.s3 import unpack_s3_uri


@mark.parametrize(
    "uri, expect",
    [
        ("/tmp/foo.txt", None),
        ("s3://foo/bar.txt", ("foo", "bar.txt")),
        ("s3://foo/bar/boo.txt", ("foo", "bar/boo.txt")),
    ],
)
def test_unpack_s3_uri(uri: str, expect: Optional[Tuple[str, str]]) -> None:
    assert unpack_s3_uri(uri) == expect
