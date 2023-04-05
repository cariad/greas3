from pathlib import Path
from unittest.mock import Mock, call

from greas3.operations import put


def test_put__directory(data_dir: Path, s3: Mock, session: Mock) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    put(data_dir, "s3://my-bucket/", session=session)

    assert upload_file.call_count == 2

    upload_file.assert_has_calls(
        [
            call(
                Bucket="my-bucket",
                ExtraArgs={"ChecksumAlgorithm": "SHA256"},
                Filename=(data_dir / "lorum.txt").as_posix(),
                Key="lorum.txt",
            ),
            call(
                Bucket="my-bucket",
                ExtraArgs={"ChecksumAlgorithm": "SHA256"},
                Filename=(data_dir / "movies" / "star-wars.txt").as_posix(),
                Key="movies/star-wars.txt",
            ),
        ]
    )


def test_put__directory__dry_run(
    data_dir: Path,
    s3: Mock,
    session: Mock,
) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    put(data_dir, "s3://my-bucket/", dry_run=True, session=session)

    upload_file.assert_not_called()


def test_put__file(lorum_path: Path, s3: Mock, session: Mock) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    put(lorum_path, "s3://my-bucket/lorum-copy.txt", session=session)

    upload_file.assert_called_with(
        Bucket="my-bucket",
        ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        Filename=lorum_path.as_posix(),
        Key="lorum-copy.txt",
    )


def test_put__file__same_filename(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
) -> None:
    upload_file = Mock()

    s3.get_object_attributes = Mock(
        return_value={
            "ObjectSize": 2054,
        }
    )

    s3.upload_file = upload_file

    put(lorum_path, "s3://my-bucket/", session=session)

    upload_file.assert_called_with(
        Bucket="my-bucket",
        ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        Filename=lorum_path.as_posix(),
        Key="lorum.txt",
    )


def test_put__file__no_upload(
    lorum_path: Path,
    s3: Mock,
    session: Mock,
) -> None:
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

    put(lorum_path, "s3://my-bucket/lorum-copy.txt", session=session)
    upload_file.assert_not_called()
