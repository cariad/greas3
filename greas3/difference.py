from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass
class Difference:
    """
    A difference between objects at the `source` and `destination` paths.
    """

    source: Union[Path, str]
    destination: Union[Path, str]
    reason: str
