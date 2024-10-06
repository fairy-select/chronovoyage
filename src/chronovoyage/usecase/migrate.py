from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.exception.domain import MigrateDomainPastTargetError

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigrateConfig, MigratePeriod
    from chronovoyage.internal.interface.database import IDatabaseConnectionWrapper
    from chronovoyage.internal.logger.logger import AppLogger


class MigrateUsecase:
    def __init__(self, *, config: MigrateConfig, logger: AppLogger) -> None:
        self._config = config
        self._logger = logger

    def migrate(self, *, target: str | None):
        with DatabaseConnector(logger=self._logger).get_connection(
            self._config.vendor, self._config.connection_info
        ) as _conn:
            created = _conn.create_if_not_exists_system_table()
            if created:
                self._logger.info("system table created")

            current = _conn.get_current_period()
            if target is not None and current is not None and target < current:
                self._logger.error("migrate operation cannot go back to the period '%s'", target)
                raise MigrateDomainPastTargetError

            for period in self._config.periods:
                if current is not None and period.period_name <= current:
                    self._logger.debug("period '%s' has already come.", period.period_name)
                    continue
                if target is not None and target < period.period_name:
                    self._logger.debug("period '%s' is in the future and migrate will stop.", period.period_name)
                    break

                period_id = self._find_or_add_period(period, _conn=_conn)

                self._logger.debug("the period '%s' is coming.", period.period_name)
                for sql in _conn.get_sqls(period.go_sql_path):
                    try:
                        _conn.execute_sql(sql)
                        self._logger.debug("executed the sql '%s'.", sql)
                    except:
                        self._logger.warning("an error occurred when executing the sql '%s'.", sql)
                        raise
                try:
                    _conn.mark_period_as_come(period_id)
                    self._logger.debug("updated the period which id is %d.", period_id)
                except:
                    self._logger.warning("an error occurred when updating the period '%s'.", period.period_name)
                    raise
                self._logger.info("the period '%s' has come.", period.period_name)

    def _find_or_add_period(self, period: MigratePeriod, *, _conn: IDatabaseConnectionWrapper) -> int:
        """

        Returns:
            int: found or inserted id.

        """
        period_id = _conn.find_period_id(period)
        if period_id is not None:
            self._logger.info("the period '%s' found.", period.period_name)
            return period_id

        self._logger.debug("adding the period '%s'.", period.period_name)
        try:
            inserted_period_id = _conn.add_period(period)
            self._logger.debug(
                "inserted the period '%s' into chronovoyage_periods. id is %d.",
                period.period_name,
                inserted_period_id,
            )
        except:
            self._logger.warning("an error occurred when adding the period '%s'.", period.period_name)
            raise
        self._logger.info("added the period '%s'.", period.period_name)
        return inserted_period_id
