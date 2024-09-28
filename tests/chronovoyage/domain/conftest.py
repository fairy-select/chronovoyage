import re

import pytest
from _pytest.fixtures import SubRequest
from helper import DEFAULT_TEST_ENV, RESOURCE_DIR
from helper.database._mariadb import truncate_mariadb_test_db

from chronovoyage.internal.config import MigrateDomainConfigFactory


class NoMariadbResourcesFoundError(FileNotFoundError):
    def __init__(self, node_name: str) -> None:
        super().__init__(f"No mariadb resources found for test {node_name}")


@pytest.fixture
def mariadb_resource_dir(request: SubRequest) -> str:
    """テストケース名に対応した mariadb の設定ディレクトリを取得する"""
    matched = re.match(r"^test_(?P<test_name>.+)$", request.node.name)
    if not matched:
        raise NoMariadbResourcesFoundError(request.node.name)
    test_name = matched.group("test_name")
    return f"{RESOURCE_DIR}/mariadb/{test_name}"


@pytest.fixture
def mariadb_migrate_domain_config(mariadb_resource_dir):
    migrate_domain_config = MigrateDomainConfigFactory().create_from_directory(mariadb_resource_dir)
    if migrate_domain_config.connection_info.database != DEFAULT_TEST_ENV["MARIADB_DATABASE"]:
        pytest.fail(f'設定ファイルの database は {DEFAULT_TEST_ENV["MARIADB_DATABASE"]} にしてください')
    try:
        yield migrate_domain_config
    finally:
        truncate_mariadb_test_db()
