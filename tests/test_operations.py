from pathlib import Path
from unittest.mock import Mock

from greas3.operations import put


def test_put(lorum: Path, s3: Mock, session: Mock) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    put(lorum, "s3://my-bucket/lorum-copy.txt", session=session)

    upload_file.assert_called_with(
        Bucket="my-bucket",
        ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        Filename=lorum.as_posix(),
        Key="lorum-copy.txt",
    )


def test_put__no_upload(lorum: Path, s3: Mock, session: Mock) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "Checksum": {
                "ChecksumSHA256": "KUPJMIoDWiIgepwgTiTPwbgVPUUC30ZmocG3iA86M90=",
            },
            "ObjectSize": 2055,
        }
    )

    s3.upload_file = upload_file

    put(lorum, "s3://my-bucket/lorum-copy.txt", session=session)
    upload_file.assert_not_called()
