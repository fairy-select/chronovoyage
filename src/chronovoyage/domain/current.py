from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.usecase.current import CurrentUsecase

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigrateConfig, MigratePeriod
    from chronovoyage.internal.logger.logger import AppLogger


class CurrentDomain:
    def __init__(self, config: MigrateConfig, *, logger: AppLogger) -> None:
        self._config = config
        self._logger = logger
        self.usecase = CurrentUsecase(config=self._config, logger=self._logger)

    def execute(self) -> MigratePeriod | None:
        return self.usecase.get_current_period()
