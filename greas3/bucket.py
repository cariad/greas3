from pathlib import Path

from boto3.session import Session

from greas3.hashes import LocalHashes, RemoteHashes
from greas3.logging import logger


class Bucket:
    """
    S3 bucket.

    `local_hashes` is the cache of local file hashes shared with the parent
    session.

    `name` is the bucket's name.

    `session` is a the Boto3 session to interact with AWS.
    """

    def __init__(
        self,
        local_hashes: LocalHashes,
        name: str,
        session: Session,
    ) -> None:
        self.local_hashes = local_hashes
        self.name = name
        self.remote_hashes = RemoteHashes(name, session)
        self.session = session

    def upload(self, path: Path, key: str) -> None:
        """
        Uploads the file at `path` to the S3 key `key` if their hashes do not
        match.
        """

        remote_key = f"s3://{self.name}/{key}"

        local_hash = self.local_hashes.get(path)
        remote_hash = self.remote_hashes.get(key)

        if local_hash == remote_hash:
            logger.debug(
                "Won't upload %s to %s because their hashes match (%s)",
                path,
                remote_key,
                local_hash.hex(),
            )
            return

        if remote_hash is None:
            logger.info(
                "Uploading %s (%s) to %s because the destination does not exist",
                path,
                local_hash.hex(),
                remote_key,
            )

        else:
            logger.info(
                "Uploading %s (%s) to %s (%s) because the hashes don't match",
                path,
                local_hash.hex(),
                remote_key,
                remote_hash.hex(),
            )

        s3 = self.session.client("s3")

        s3.upload_file(
            Filename=path.as_posix(),
            Bucket=self.name,
            Key=key,
            ExtraArgs={"ChecksumAlgorithm": "SHA256"},
        )
