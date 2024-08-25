import pytest
from helper import RESOURCE_DIR

from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.logger import get_default_logger


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()
        self.config_factory = MigrateDomainConfigFactory()

    def test_ddl_only(self) -> None:
        config_dir = f"{RESOURCE_DIR}/mariadb/ddl_only"
        migrate_domain_config = self.config_factory.create_from_directory(config_dir)
        MigrateDomain(migrate_domain_config, logger=self.logger).execute()

    def test_period_name_invalid(self) -> None:
        config_dir = f"{RESOURCE_DIR}/mariadb/period_name_invalid"
        with pytest.raises(MigrateConfigVersionNameInvalidError):
            _ = self.config_factory.create_from_directory(config_dir)

    def test_both_sqls_missing(self) -> None:
        config_dir = f"{RESOURCE_DIR}/mariadb/both_sqls_missing"
        with pytest.raises(MigrateConfigSqlMissingError):
            _ = self.config_factory.create_from_directory(config_dir)

    def test_go_sql_missing(self) -> None:
        config_dir = f"{RESOURCE_DIR}/mariadb/go_sql_missing"
        with pytest.raises(MigrateConfigGoSqlMissingError):
            _ = self.config_factory.create_from_directory(config_dir)

    def test_return_sql_missing(self) -> None:
        config_dir = f"{RESOURCE_DIR}/mariadb/return_sql_missing"
        with pytest.raises(MigrateConfigReturnSqlMissingError):
            _ = self.config_factory.create_from_directory(config_dir)
