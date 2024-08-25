import pytest

from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.exception.config import MigrateConfigVersionNameInvalidError, MigrateConfigSqlMissingError, \
    MigrateConfigGoSqlMissingError, MigrateConfigReturnSqlMissingError
from chronovoyage.logger import get_default_logger
from helper import RESOURCE_DIR


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()
        self.config_factory = MigrateDomainConfigFactory()

    def test_ddl_only(self) -> None:
        migrate_domain_config = self.config_factory.create_from_directory(
            f"{RESOURCE_DIR}/mariadb/ddl_only"
        )
        MigrateDomain(migrate_domain_config, logger=self.logger).execute()

    def test_period_name_invalid(self) -> None:
        with pytest.raises(MigrateConfigVersionNameInvalidError):
            _ = self.config_factory.create_from_directory(
                f"{RESOURCE_DIR}/mariadb/period_name_invalid"
            )

    def test_both_sqls_missing(self) -> None:
        with pytest.raises(MigrateConfigSqlMissingError):
            _ = self.config_factory.create_from_directory(
                f"{RESOURCE_DIR}/mariadb/both_sqls_missing"
            )

    def test_go_sql_missing(self) -> None:
        with pytest.raises(MigrateConfigGoSqlMissingError):
            _ = self.config_factory.create_from_directory(
                f"{RESOURCE_DIR}/mariadb/go_sql_missing"
            )

    def test_return_sql_missing(self) -> None:
        with pytest.raises(MigrateConfigReturnSqlMissingError):
            _ = self.config_factory.create_from_directory(
                f"{RESOURCE_DIR}/mariadb/return_sql_missing"
            )
