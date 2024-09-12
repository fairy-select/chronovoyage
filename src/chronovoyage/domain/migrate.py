from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.usecase.migrate import MigrateUsecase

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.internal.config import MigrateDomainConfig


class MigrateDomain:
    def __init__(self, config: MigrateDomainConfig, *, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def execute(self, *, target: str | None = None) -> None:
        MigrateUsecase(config=self._config, logger=self._logger).migrate(target=target)
