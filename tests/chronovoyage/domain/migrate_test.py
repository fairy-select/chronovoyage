import pytest
from helper import TESTS_DIR

from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.logger import get_default_logger

logger = get_default_logger()


class TestMigrateDomain:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.config_factory = MigrateDomainConfigFactory()

    def test_migrate_ddl_only_create_db(self) -> None:
        migrate_domain_config = self.config_factory.create_from_directory(
            f"{TESTS_DIR}/resource/mariadb/ddl_only_create_db"
        )
        MigrateDomain(migrate_domain_config, logger=logger).execute()
