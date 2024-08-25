from logging import Logger

from chronovoyage.internal.config import MigrateDomainConfig
from chronovoyage.usecase.migrate import MigrateUsecase


class MigrateDomain:
    def __init__(self, config: MigrateDomainConfig, *, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def execute(self) -> None:
        MigrateUsecase(config=self._config, logger=self._logger).migrate()
