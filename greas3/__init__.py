from importlib.resources import open_text

from greas3.operations import put

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "put",
]
