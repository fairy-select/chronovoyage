import re

import pytest
from _pytest.fixtures import SubRequest
from support import RESOURCE_DIR

from chronovoyage.internal.type.enum import DatabaseVendorEnum


class NoMariadbResourcesFoundError(FileNotFoundError):
    def __init__(self, node_name: str) -> None:
        super().__init__(f"No mariadb resources found for test {node_name}")


class NoResourcesFoundError(FileNotFoundError):
    def __init__(self, vendor: DatabaseVendorEnum, node_name: str) -> None:
        super().__init__(f"No {vendor.value} resources found for test {node_name}")


@pytest.fixture
def resource_dir_factory(request: SubRequest):
    """テストケース名に対応した設定ディレクトリを取得する"""

    class ResourceDir:
        @classmethod
        def get_directory(cls, vendor: DatabaseVendorEnum) -> str:
            matched = re.match(r"^(?P<test_name>test_.+)$", request.node.name)
            if not matched:
                raise NoResourcesFoundError(vendor, request.node.name)
            test_name = matched.group("test_name")
            return f"{RESOURCE_DIR}/{vendor.value}/{test_name}"

    return ResourceDir
