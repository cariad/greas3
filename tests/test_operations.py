from unittest.mock import Mock

from greas3.difference import Difference
from greas3.operations import difference


def test_difference__size(session: Mock) -> None:
    get_object_attributes = Mock(
        return_value={
            "ObjectSize": 3,
        }
    )

    s3 = Mock()
    s3.get_object_attributes = get_object_attributes

    client = Mock(return_value=s3)
    session.client = client

    result = difference("README.md", "my-bucket", "readme.md", session=session)

    client.assert_called_once_with("s3")

    get_object_attributes.assert_called_once_with(
        Bucket="my-bucket",
        Key="readme.md",
        ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
    )

    assert result == Difference(
        source="README.md",
        destination="readme.md",
        reason="Destination is a different length",
    )
