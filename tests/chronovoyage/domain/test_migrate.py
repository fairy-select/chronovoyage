import pytest
from helper.database.mariadb import get_default_mariadb_connection

from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.logger import get_default_logger


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()
        self.config_factory = MigrateDomainConfigFactory()

    def test_ddl_only(self, mariadb_resource_dir) -> None:
        # given
        migrate_domain_config = self.config_factory.create_from_directory(mariadb_resource_dir)
        # when
        MigrateDomain(migrate_domain_config, logger=self.logger).execute()
        # then
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SHOW TABLES")
            assert {table for (table,) in cursor} == {"user", "category"}

    def test_period_name_invalid(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigVersionNameInvalidError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SHOW TABLES")
            assert cursor.rowcount == 0

    def test_both_sqls_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SHOW TABLES")
            assert cursor.rowcount == 0

    def test_go_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigGoSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SHOW TABLES")
            assert cursor.rowcount == 0

    def test_return_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigReturnSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SHOW TABLES")
            assert cursor.rowcount == 0
