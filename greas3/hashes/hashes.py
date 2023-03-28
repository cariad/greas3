from typing import Callable, Dict, Optional


class Hashes:
    """
    Cache of object hashes.
    """

    def __init__(self) -> None:
        self.cache: Dict[str, Optional[bytes]] = {}

    def populate_get(
        self,
        key: str,
        populate: Callable[[str], Optional[bytes]],
    ) -> Optional[bytes]:
        """
        Gets the hash of the object `key`.

        Populates the cache by calling `populate` if the key is not present.
        """

        if key not in self.cache:
            self.cache[key] = populate(key)

        return self.cache[key]
