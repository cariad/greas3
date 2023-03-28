from base64 import b64decode
from typing import Optional

from boto3.session import Session

from greas3.hashes.hashes import Hashes


class RemoteHashes(Hashes):
    """
    Cache of remote object hashes.

    `bucket` is the name of the S3 bucket to read.

    `session` is the Boto3 session to interact with AWS.
    """

    def __init__(self, bucket: str, session: Session) -> None:
        super().__init__()

        self.bucket = bucket
        self.session = session

    def get(self, key: str) -> Optional[bytes]:
        """
        Gets the hash of the S3 object at `key`.
        """

        return self.populate_get(key, self.hash)

    def hash(self, key: str) -> Optional[bytes]:
        """
        Circumvents the cache to get the hash of the S3 object at `key`.
        """

        s3 = self.session.client("s3")

        try:
            response = s3.get_object_attributes(
                Bucket=self.bucket,
                Key=key,
                ObjectAttributes=["Checksum"],
            )
            c = response["Checksum"]["ChecksumSHA256"]
            return b64decode(c)

        except s3.exceptions.NoSuchKey:
            return None
