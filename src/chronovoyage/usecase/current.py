from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.exception.current import CurrentDbCurrentPeriodNotInMigrateConfigError

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.internal.config import MigrateDomainConfig, MigratePeriod


class CurrentUsecase:
    def __init__(self, *, config: MigrateDomainConfig, logger: Logger) -> None:
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

        raise CurrentDbCurrentPeriodNotInMigrateConfigError(current_period)
