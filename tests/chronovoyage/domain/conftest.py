import re

import pytest
from _pytest.fixtures import SubRequest
from helper import RESOURCE_DIR, DEFAULT_TEST_ENV
from helper.database.mariadb import truncate_mariadb_test_db

from chronovoyage.internal.config import MigrateDomainConfigFactory


@pytest.fixture
def mariadb_resource_dir(request: SubRequest) -> str:
    """テストケース名に対応した mariadb の設定ディレクトリを取得する"""
    test_name = re.match(r"^test_(?P<test_name>.+)$", request.node.name).group("test_name")
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
