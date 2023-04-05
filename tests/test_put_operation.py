from pathlib import Path
from unittest.mock import Mock, patch

from slash3 import S3Uri

from greas3.put_operation import PutOperation


def test_are_same(
    put_operation: PutOperation,
    lorum_path: Path,
    lorum_uri: S3Uri,
    session: Mock,
) -> None:
    with patch("greas3.put_operation.are_same") as are_same:
        put_operation.are_same(session)

    are_same.assert_called_once_with(lorum_path, lorum_uri, session)


def test_are_same__cache(
    put_operation: PutOperation,
    session: Mock,
) -> None:
    with patch("greas3.put_operation.are_same") as are_same:
        put_operation.are_same(session)
        put_operation.are_same(session)

    assert are_same.call_count == 1
