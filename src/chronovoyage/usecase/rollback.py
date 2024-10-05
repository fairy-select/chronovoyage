from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.exception.migrate import RollbackFutureTargetError, RollbackSystemTableNotExistError

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.internal.config import MigrateConfig


class RollbackUsecase:
    def __init__(self, *, config: MigrateConfig, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def rollback(self, *, target: str | None):
        with DatabaseConnector(logger=self._logger).get_connection(
            self._config.vendor, self._config.connection_info
        ) as _conn:
            if not _conn.system_table_exists():
                self._logger.error("system table does not exist")
                raise RollbackSystemTableNotExistError

            current = _conn.get_current_period()
            if target is not None and current is not None and current < target:
                self._logger.error("rollback operation cannot go forward to the period '%s'", target)
                raise RollbackFutureTargetError

            for period in reversed(self._config.periods):
                if current is not None and current < period.period_name:
                    self._logger.debug("period '%s' has not come yet.", period.period_name)
                    continue
                if target is not None and period.period_name <= target:
                    self._logger.debug("period '%s' is now or the past and migrate will stop.", period.period_name)
                    break

                period_id = _conn.find_period_id(period)
                if period_id is None:
                    # TODO: error log and raise Exception
                    return

                self._logger.debug("going back to the period '%s'.", period.period_name)
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
                    self._logger.warning("an error occurred when updating the period '%s'.", period.period_name)
                    raise
                self._logger.info("went back to the period '%s'.", period.period_name)
