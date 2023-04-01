from pathlib import Path
from unittest.mock import Mock

from pytest import fixture

from greas3.logging import logger

logger.setLevel("DEBUG")


@fixture
def data_dir() -> Path:
    return Path(__file__).parent / "data"


@fixture
def lorum(data_dir: Path) -> Path:
    return data_dir / "lorum.txt"


@fixture
def s3() -> Mock:
    return Mock()


@fixture
def session(s3: Mock) -> Mock:
    session = Mock()
    session.client = Mock(return_value=s3)
    return session
