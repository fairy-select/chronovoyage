import pytest

from chronovoyage.config.migrate import MigrateDomainConfigFactory
from chronovoyage.domain.migrate import MigrateDomain
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
