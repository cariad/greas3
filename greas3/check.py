from base64 import b64decode
from os.path import getsize
from pathlib import Path

from boto3.session import Session
from slash3 import S3Uri

from greas3.local import has_expected_hash
from greas3.logging import logger


def are_same(local: Path, uri: S3Uri, session: Session) -> bool:
    """
    Checks if the file at `local` appears to be identical to the remote object
    at `uri`.
    """

    s3 = session.client("s3")

    try:
        response = s3.get_object_attributes(
            Bucket=uri.bucket,
            Key=uri.key.key,
            ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
        )

    except s3.exceptions.NoSuchKey:
        logger.debug("The remote doesn't exist")
        return False

    if response["ObjectSize"] != getsize(local):
        logger.debug("The objects are different lengths")
        return False

    if "ObjectParts" in response:
        offset = 0

        while True:
            parts = response["ObjectParts"]

            try:
                for part in parts["Parts"]:
                    length = part["Size"]
                    expect = b64decode(part["ChecksumSHA256"])

                    if not has_expected_hash(
                        local,
                        expect,
                        offset=offset,
                        length=length,
                    ):
                        logger.debug("A chunk has a different hash")
                        return False

                    offset += length

            except KeyError as ex:
                logger.error(
                    "No %s in get_object_attributes response (%s)",
                    str(ex),
                    repr(response),
                )
                raise

            total_parts = parts.get("TotalPartsCount", 0)
            next_marker = parts.get("NextPartNumberMarker", None)

            if next_marker is None or next_marker <= total_parts:
                logger.debug("All parts have expected hash")
                return True

            response = s3.get_object_attributes(
                Bucket=uri.bucket,
                Key=uri.key.key,
                ObjectAttributes=["ObjectParts"],
                PartNumberMarker=next_marker,
            )

    expect = b64decode(response["Checksum"]["ChecksumSHA256"])

    if not has_expected_hash(local, expect):
        logger.debug("The objects have different hashes")
        return False

    logger.debug("The objects have the same hash")
    return True
