from pathlib import Path
from unittest.mock import Mock

from pytest import fixture
from slash3 import S3Uri

from greas3.logging import logger
from greas3.put_operation import PutOperation

logger.setLevel("DEBUG")


@fixture
def data_dir() -> Path:
    return Path(__file__).parent / "data"


@fixture
def lorum_path(data_dir: Path) -> Path:
    return data_dir / "lorum.txt"


@fixture
def lorum_uri() -> S3Uri:
    return S3Uri("s3://books/free/lorum.txt")


@fixture
def s3() -> Mock:
    return Mock()


@fixture
def session(s3: Mock) -> Mock:
    session = Mock()
    session.client = Mock(return_value=s3)
    return session


@fixture
def put_operation(lorum_path: Path, lorum_uri: S3Uri) -> PutOperation:
    return PutOperation(
        lorum_path,
        "lorum.txt",
        lorum_uri,
        "free/lorum.txt",
    )
