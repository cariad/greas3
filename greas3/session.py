from typing import Optional

from boto3.session import Session as Boto3Session

from greas3.bucket import Bucket
from greas3.hashes import LocalHashes


class Session:
    """
    Greas3 session.

    `boto3_session` is an optional Boto3 session to interact with AWS.
    """

    def __init__(
        self,
        boto3_session: Optional[Boto3Session] = None,
    ) -> None:
        self.boto3_session = boto3_session
        self.local_hashes = LocalHashes()

    def bucket(
        self,
        name: str,
        boto3_session: Optional[Boto3Session] = None,
    ) -> Bucket:
        """
        Gets a client for the bucket named `name`.

        `boto3_session` is an optional Boto3 session to interact with AWS.
        """

        return Bucket(
            self.local_hashes,
            name,
            boto3_session or self.boto3_session or Boto3Session(),
        )
