import pytest

from helper.database import DatabaseHelper


@pytest.fixture
def database_helper() -> DatabaseHelper:
    return DatabaseHelper()
