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
        self.usecase = MigrateUsecase(config=self._config, logger=self._logger)

    def execute(self, *, target: str | None = None) -> None:
        if target is not None and target not in map(lambda _period: _period.period_name, self._config.periods):
            self._logger.error("period '%s' is not a valid period name.", target)
            raise ValueError("unknown target")

        self.usecase.migrate(target=target)
