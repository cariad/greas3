from pathlib import Path
from typing import Union


class Difference:
    """
    A difference between objects at the `source` and `destination` paths.
    """

    def __init__(
        self,
        source: Union[Path, str],
        destination: Union[Path, str],
        reason: str,
    ) -> None:
        self.source = source
        self.destination = destination
        self.reason = reason
