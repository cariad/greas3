from base64 import b64decode
from os.path import getsize
from pathlib import Path
from typing import Optional, Union

from boto3.session import Session

from greas3.difference import Difference
from greas3.local import has_expected_hash
from greas3.logging import logger


def difference(
    path: Union[Path, str],
    bucket: str,
    key: str,
    session: Optional[Session] = None,
) -> Optional[Difference]:
    """
    Describes the difference between the local file at `path` and remote file
    in bucket `bucket` at key `key`.
    """

    # It's cheap to get the local file's length. Let's skip all the hash
    # checks if the remote object is a different length.
    expect_length = getsize(path)

    session = session or Session()
    s3 = session.client("s3")

    try:
        response = s3.get_object_attributes(
            Bucket=bucket,
            Key=key,
            ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
        )

    except s3.exceptions.NoSuchKey:
        return Difference(path, key, "Destination does not exist")

    if response["ObjectSize"] != expect_length:
        return Difference(path, key, "Destination is a different length")

    if "ObjectParts" in response:
        offset = 0

        while True:
            for part in response["ObjectParts"]["Parts"]:
                length = part["Size"]
                expect = b64decode(part["ChecksumSHA256"])

                if not has_expected_hash(path, expect, offset=offset, length=length):
                    return Difference(path, key, "Hashes do not match")

                offset += length

            next_marker = response["ObjectParts"].get("NextPartNumberMarker")

            if next_marker is None:
                return None

            response = s3.get_object_attributes(
                Bucket=bucket,
                Key=key,
                ObjectAttributes=["ObjectParts"],
                PartNumberMarker=next_marker,
            )

    expect = b64decode(response["Checksum"]["ChecksumSHA256"])

    if has_expected_hash(path, expect):
        return None

    return Difference(path, key, "Hashes do not match")


def put(
    path: Path,
    bucket: str,
    key: str,
    session: Optional[Session] = None,
) -> None:
    """
    Uploads the file at `path` to the S3 key `key` if it is new or different.
    """

    session = session or Session()

    d = difference(path, bucket, key, session)

    if d is None:
        return

    logger.info(d.reason)
    s3 = session.client("s3")

    s3.upload_file(
        Bucket=bucket,
        ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        Filename=path.as_posix(),
        Key=key,
    )
