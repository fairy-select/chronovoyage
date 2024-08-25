import re
from typing import Any, Generator

import pytest
from _pytest.fixtures import SubRequest
from helper import RESOURCE_DIR
from helper.database.mariadb import truncate_mariadb_test_db


@pytest.fixture
def mariadb_resource_dir(request: SubRequest) -> Generator[str, Any, None]:
    """テストケース名に対応した mariadb の設定ディレクトリを取得する"""
    test_name = re.match(r"^test_(?P<test_name>.+)$", request.node.name).group("test_name")
    yield f"{RESOURCE_DIR}/mariadb/{test_name}"
    truncate_mariadb_test_db()
