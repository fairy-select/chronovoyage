import pytest

from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.exception.config import (
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

    def test_ddl_only(self, mariadb_resource_dir) -> None:
        migrate_domain_config = self.config_factory.create_from_directory(mariadb_resource_dir)
        MigrateDomain(migrate_domain_config, logger=self.logger).execute()

    def test_period_name_invalid(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigVersionNameInvalidError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_both_sqls_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_go_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigGoSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_return_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigReturnSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)
