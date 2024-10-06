from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.exception.domain import MigrateDomainUnknownTargetError
from chronovoyage.usecase.migrate import MigrateUsecase

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigrateConfig
    from chronovoyage.internal.logger.logger import AppLogger


class MigrateDomain:
    def __init__(self, config: MigrateConfig, *, logger: AppLogger) -> None:
        self._config = config
        self._logger = logger
        self.usecase = MigrateUsecase(config=self._config, logger=self._logger)

    def execute(self, *, target: str | None = None) -> None:
        if target is not None and target not in (period.period_name for period in self._config.periods):
            self._logger.error("period '%s' is not a valid period name.", target)
            raise MigrateDomainUnknownTargetError

        self.usecase.migrate(target=target)
