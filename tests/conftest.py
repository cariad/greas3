from unittest.mock import Mock

from pytest import fixture


@fixture
def session() -> Mock:
    return Mock()
