from pathlib import Path

from boto3.session import Session
from slash3 import S3Uri

from greas3.check import are_same


class PutOperation:
    """
    An enqueued upload operation.
    """

    def __init__(
        self,
        path: Path,
        relative_path: str,
        uri: S3Uri,
        relative_uri: str,
    ) -> None:
        self.path = path
        self.relative_path = relative_path
        self.uri = uri
        self.relative_uri = relative_uri

    def same(self, session: Session) -> bool:
        """
        Determines whether or not the local and remote file seem to be
        identical.
        """

        return are_same(self.path, self.uri, session)
