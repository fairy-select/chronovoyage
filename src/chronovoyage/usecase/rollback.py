from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.exception.domain import (
    RollbackDomainFutureTargetError,
    RollbackDomainMigratedPeriodNotInMigrateConfigError,
    RollbackDomainSystemTableNotExistError,
)

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigrateConfig
    from chronovoyage.internal.logger.logger import AppLogger


class RollbackUsecase:
    def __init__(self, *, config: MigrateConfig, logger: AppLogger) -> None:
        self._config = config
        self._logger = logger

    def rollback(self, *, target: str | None):
        with DatabaseConnector(logger=self._logger).get_connection(
            self._config.vendor, self._config.connection_info
        ) as _conn:
            if not _conn.system_table_exists():
                self._logger.error("system table does not exist")
                raise RollbackDomainSystemTableNotExistError

            current = _conn.get_current_period()
            if target is not None and current is not None and current < target:
                self._logger.error("rollback operation cannot go forward to the period '%s'", target)
                raise RollbackDomainFutureTargetError

            period_name_to_period = {period.period_name: period for period in self._config.periods}
            for period_id, period_name in _conn.get_all_come_periods(reverse=True):
                if current is not None and current < period_name:
                    self._logger.debug("period '%s' has not come yet.", period_name)
                    continue
                if target is not None and period_name <= target:
                    self._logger.debug("period '%s' is now or the past and migrate will stop.", period_name)
                    break

                period = period_name_to_period.get(period_name)
                if period is None:
                    raise RollbackDomainMigratedPeriodNotInMigrateConfigError(period_name)

                self._logger.debug("going back to the period '%s'.", period_name)
                for sql in _conn.get_sqls(period.return_sql_path):
                    try:
                        _conn.execute_sql(sql)
                        self._logger.debug("executed the sql '%s'.", sql)
                    except:
                        self._logger.warning("an error occurred when executing the sql '%s'.", sql)
                        raise
                try:
                    _conn.mark_period_as_not_come(period_id)
                    self._logger.debug("updated the period which id is %d.", period_id)
                except:
                    self._logger.warning("an error occurred when updating the period '%s'.", period_name)
                    raise
                self._logger.info("went back to the period '%s'.", period_name)
