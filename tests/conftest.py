from pathlib import Path
from unittest.mock import Mock

from pytest import fixture

from greas3.logging import logger

logger.setLevel("DEBUG")


@fixture
def lorum() -> Path:
    return Path(__file__).parent / "lorum.txt"


@fixture
def s3() -> Mock:
    return Mock()


@fixture
def session(s3: Mock) -> Mock:
    session = Mock()
    session.client = Mock(return_value=s3)
    return session
