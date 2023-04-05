from pathlib import Path
from unittest.mock import Mock

from pytest import fixture, raises
from slash3 import S3Uri

from greas3.check import are_same


@fixture
def uri() -> S3Uri:
    return S3Uri("s3://my-bucket/lorum-copy.txt")


def test_are_same__different_hash(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {"ChecksumSHA256": ""},
            "ObjectSize": 2055,
        }
    )

    assert not are_same(lorum_path, uri, session)


def test_are_same__different_length(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    get_object_attributes = Mock(return_value={"ObjectSize": 3})

    s3.get_object_attributes = get_object_attributes

    result = are_same(lorum_path, uri, session)

    get_object_attributes.assert_called_once_with(
        Bucket="my-bucket",
        Key="lorum-copy.txt",
        ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
    )

    assert not result


def test_are_same__different_parts_hash(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        return_value={
            "ObjectParts": {
                "Parts": [
                    {
                        "Size": 512,
                        "ChecksumSHA256": "",
                    }
                ]
            },
            "ObjectSize": 2055,
        }
    )

    assert not are_same(lorum_path, uri, session)


def test_are_same__different_parts_hash__multiple(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        side_effect=[
            {
                "ObjectParts": {
                    "NextPartNumberMarker": 1,
                    "Parts": [
                        {
                            "Size": 512,
                            "ChecksumSHA256": "ogxgwa5eW+Hb+xVVa+cRw/uoNIgey8JfT2GITb1sRT4=",  # noqa: E501
                        }
                    ],
                },
                "ObjectSize": 2055,
            },
            {
                "ObjectParts": {
                    "Parts": [
                        {
                            "Size": 512,
                            "ChecksumSHA256": "",
                        }
                    ]
                },
            },
        ]
    )

    assert not are_same(lorum_path, uri, session)


def test_are_same__does_not_exist(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    no_such_key = ValueError

    exceptions = Mock()
    exceptions.NoSuchKey = no_such_key

    s3.exceptions = exceptions
    s3.get_object_attributes = Mock(side_effect=ValueError)

    assert not are_same(lorum_path, uri, session)


def test_are_same__invalid_response(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        return_value={
            "ObjectParts": {
                "Ports": [
                    {
                        "Size": 512,
                        "ChecksumSHA256": "",
                    }
                ]
            },
            "ObjectSize": 2055,
        }
    )

    with raises(KeyError):
        are_same(lorum_path, uri, session)


def test_are_same__same_hash(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {
                "ChecksumSHA256": "KUPJMIoDWiIgepwgTiTPwbgVPUUC30ZmocG3iA86M90=",
            },
            "ObjectSize": 2055,
        }
    )

    assert are_same(lorum_path, uri, session)


def test_are_same__same_parts_hash__multiple(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
    uri: S3Uri,
) -> None:
    s3.get_object_attributes = Mock(
        side_effect=[
            {
                "ObjectParts": {
                    "NextPartNumberMarker": 1,
                    "Parts": [
                        {
                            "Size": 512,
                            "ChecksumSHA256": "ogxgwa5eW+Hb+xVVa+cRw/uoNIgey8JfT2GITb1sRT4=",  # noqa: E501
                        }
                    ],
                },
                "ObjectSize": 2055,
            },
            {
                "ObjectParts": {
                    "Parts": [
                        {
                            "Size": 512,
                            "ChecksumSHA256": "BjUOo+SH4qnMBqrkwbGsqgmWo4sekhx7OJVSdWEQW4k=",  # noqa: E501
                        }
                    ]
                },
            },
        ]
    )

    assert are_same(lorum_path, uri, session)
