from pathlib import Path
from unittest.mock import Mock

from pytest import fixture

from greas3.logging import logger

logger.setLevel("DEBUG")


@fixture
def lorum() -> Path:
    return Path() / "tests" / "lorum.txt"


@fixture
def session() -> Mock:
    return Mock()
