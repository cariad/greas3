from re import match
from typing import Optional, Tuple


def unpack_s3_uri(uri: str) -> Optional[Tuple[str, str]]:
    """
    Unpacks an S3 URI into its component bucket and key.
    """

    if m := match(r"s3:\/\/([^/]*)\/(.*)", uri):
        return m.group(1), m.group(2)

    return None
