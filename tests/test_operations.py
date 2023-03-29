from pathlib import Path
from unittest.mock import Mock

from greas3.difference import Difference
from greas3.operations import difference, put


def test_difference__different_hash(lorum: Path, session: Mock) -> None:
    s3 = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {
                "ChecksumSHA256": "",
            },
            "ObjectSize": 2055,
        }
    )

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result == Difference(
        source=lorum,
        destination="readme.md",
        reason="Hashes do not match",
    )


def test_difference__different_length(lorum: Path, session: Mock) -> None:
    get_object_attributes = Mock(
        return_value={
            "ObjectSize": 3,
        }
    )

    s3 = Mock()
    s3.get_object_attributes = get_object_attributes

    client = Mock(return_value=s3)
    session.client = client

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    client.assert_called_once_with("s3")

    get_object_attributes.assert_called_once_with(
        Bucket="my-bucket",
        Key="readme.md",
        ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
    )

    assert result == Difference(
        source=lorum,
        destination="readme.md",
        reason="Destination is a different length",
    )


def test_difference__different_parts_hash(lorum: Path, session: Mock) -> None:
    s3 = Mock()

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

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result == Difference(
        source=lorum,
        destination="readme.md",
        reason="Hashes do not match",
    )


def test_difference__different_parts_hash__multiple(lorum: Path, session: Mock) -> None:
    s3 = Mock()

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

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result == Difference(
        source=lorum,
        destination="readme.md",
        reason="Hashes do not match",
    )


def test_difference__does_not_exist(lorum: Path, session: Mock) -> None:
    no_such_key = ValueError

    exceptions = Mock()
    exceptions.NoSuchKey = no_such_key

    s3 = Mock()
    s3.exceptions = exceptions
    s3.get_object_attributes = Mock(side_effect=ValueError)

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result == Difference(
        source=lorum,
        destination="readme.md",
        reason="Destination does not exist",
    )


def test_difference__same_hash(lorum: Path, session: Mock) -> None:
    s3 = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {
                "ChecksumSHA256": "KUPJMIoDWiIgepwgTiTPwbgVPUUC30ZmocG3iA86M90=",
            },
            "ObjectSize": 2055,
        }
    )

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result is None


def test_difference__same_parts_hash__multiple(lorum: Path, session: Mock) -> None:
    s3 = Mock()

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

    session.client = Mock(return_value=s3)

    result = difference(lorum, "my-bucket", "readme.md", session=session)

    assert result is None


def test_put(lorum: Path, session: Mock) -> None:
    upload_file = Mock()

    s3 = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    session.client = Mock(return_value=s3)

    put(lorum, "my-bucket", "lorum.md", session=session)
    upload_file.assert_called_with(
        Bucket="my-bucket",
        ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        Filename=lorum.as_posix(),
        Key="lorum.md",
    )


def test_put__no_upload(lorum: Path, session: Mock) -> None:
    upload_file = Mock()

    s3 = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {
                "ChecksumSHA256": "KUPJMIoDWiIgepwgTiTPwbgVPUUC30ZmocG3iA86M90=",
            },
            "ObjectSize": 2055,
        }
    )

    s3.upload_file = upload_file

    session.client = Mock(return_value=s3)

    put(lorum, "my-bucket", "lorum.md", session=session)
    upload_file.assert_not_called()
