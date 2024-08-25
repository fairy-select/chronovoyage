import pytest

from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.logger import get_default_logger
from helper import TESTS_DIR

logger = get_default_logger()


class TestMigrateDomain:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.config_factory = MigrateDomainConfigFactory()

    def test_migrate_ddl_only(self, database_helper) -> None:
        migrate_domain_config = self.config_factory.create_from_directory(f"{TESTS_DIR}/resource/mariadb/ddl_only")
        MigrateDomain(migrate_domain_config, logger=logger).execute()
