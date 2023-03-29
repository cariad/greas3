from pathlib import Path

from greas3.local import has_expected_hash


def test_has_expected_hash__chunk(lorum: Path) -> None:
    expect = b"I6\xd5zN\xfc&%\x83@7i\x07\x8ej\xa8\xe6\xaca\xb2h \x08\x0c\xf9\xd9\x1a\xf7\xb5\xd8\xc62"  # noqa: E501
    assert has_expected_hash(lorum, expect, offset=1024, length=128)


def test_has_expected_hash__entire(lorum: Path) -> None:
    expect = b')C\xc90\x8a\x03Z" z\x9c N$\xcf\xc1\xb8\x15=E\x02\xdfFf\xa1\xc1\xb7\x88\x0f:3\xdd'  # noqa: E501
    assert has_expected_hash(lorum, expect)
