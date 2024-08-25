import re

import pytest
from _pytest.fixtures import SubRequest
from helper import RESOURCE_DIR


@pytest.fixture
def mariadb_resource_dir(request: SubRequest) -> str:
    test_name = re.match(r"^test_(?P<test_name>.+)$", request.node.name).group("test_name")
    return f"{RESOURCE_DIR}/mariadb/{test_name}"
