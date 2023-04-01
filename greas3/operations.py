from pathlib import Path
from typing import Optional, Union

from ansiscape import green, heavy, yellow
from boto3.session import Session
from slash3 import S3Uri

from greas3.logging import logger
from greas3.put_operations import PutOperations


def put(
    path: Union[Path, str],
    uri: Union[S3Uri, str],
    dry_run: bool = False,
    session: Optional[Session] = None,
    silent: bool = False,
) -> None:
    """
    Uploads a local file to S3 as long as the remote file doesn't exist or is
    different.

    `dry_run` will log the uploads but not perform them.

    `session` is an optional Boto3 session. A new session will be created if
    omitted.

    `silent` mutes all progress logging.
    """

    path = Path(path) if isinstance(path, str) else path
    uri = S3Uri(uri) if isinstance(uri, str) else uri

    if path.is_dir():
        operations = PutOperations.from_dir(path, uri)
        if not silent:
            logger.info(
                "%s   %s",
                heavy(path.as_posix().ljust(operations.longest_relative_path)),
                heavy("s3://", yellow(uri.bucket), "/", uri.key.key),
            )

    else:
        operations = PutOperations.from_file(path, uri)

    session = session or Session()
    s3 = session.client("s3")

    for op in operations.operations:
        same = op.same(session)

        if not silent:
            logger.info(
                "%s %s %s",
                op.relative_path.ljust(operations.longest_relative_path),
                green("=") if same else yellow(">"),
                op.relative_uri,
            )

        if same or dry_run:
            continue

        s3.upload_file(
            Bucket=op.uri.bucket,
            ExtraArgs={"ChecksumAlgorithm": "SHA256"},
            Filename=op.path.as_posix(),
            Key=op.uri.key.key,
        )
