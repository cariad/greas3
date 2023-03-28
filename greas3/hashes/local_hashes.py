from hashlib import sha256
from pathlib import Path

from greas3.hashes.hashes import Hashes


class LocalHashes(Hashes):
    """
    Cache of local file hashes.
    """

    def get(self, path: Path) -> bytes:
        """
        Gets the hash of the local file at `path`.

        Raises `ValueError` if the file has no hash.
        """

        key = path.resolve().absolute().as_posix()
        value = self.populate_get(key, self.hash)

        if not value:
            raise ValueError(f"{path} has no hash")

        return value

    @staticmethod
    def hash(path: str) -> bytes:
        """
        Circumvents the cache to get the hash of the local file at `path`.
        """

        digest = sha256(usedforsecurity=False)

        with open(path, "rb") as f:
            while True:
                if data := f.read(4096):
                    digest.update(data)
                else:
                    return digest.digest()
