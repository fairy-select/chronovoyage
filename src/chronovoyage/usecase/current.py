from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.exception.domain import CurrentDomainDbCurrentPeriodNotInMigrateConfigError

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigrateConfig, MigratePeriod
    from chronovoyage.internal.logger.logger import AppLogger


class CurrentUsecase:
    def __init__(self, *, config: MigrateConfig, logger: AppLogger) -> None:
        self._config = config
        self._logger = logger

    def get_current_period(self) -> MigratePeriod | None:
        with DatabaseConnector(logger=self._logger).get_connection(
            self._config.vendor, self._config.connection_info
        ) as _conn:
            current_period = _conn.get_current_period()

        if current_period is None:
            return None

        for period in self._config.periods:
            if period.period_name == current_period:
                return period

        raise CurrentDomainDbCurrentPeriodNotInMigrateConfigError(current_period)
