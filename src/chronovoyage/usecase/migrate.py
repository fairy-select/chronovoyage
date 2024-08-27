from logging import Logger

from chronovoyage.internal.config import MigrateDomainConfig
from chronovoyage.internal.database.connection import DatabaseConnector


class MigrateUsecase:
    def __init__(self, *, config: MigrateDomainConfig, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def migrate(self):
        with DatabaseConnector(logger=self._logger).get_connection(self._config.vendor, self._config.connection_info) as _conn:
            for period in self._config.periods:
                self._logger.debug("adding the period '%s'.", period.period_name)
                try:
                    with _conn.begin() as conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO chronovoyage_periods (period_name, language, description) VALUES (?, ?, ?)", (period.period_name, period.language, period.description))
                        inserted_period_id = cursor.lastrowid
                        self._logger.debug("inserted the period '%s' into chronovoyage_periods. id is %d.", period.period_name, inserted_period_id)
                except:
                    self._logger.warning("an error occurred when adding the period '%s'.", period.period_name)
                    raise
                self._logger.info("added the period '%s'.", period.period_name)

                self._logger.debug("the period '%s' is coming.", period.period_name)
                with open(period.go_sql_path) as f:
                    file_content = f.read()
                    self._logger.debug("read file content of %s.", period.go_sql_path)
                for sql in [sql.strip() for sql in file_content.strip().split(";") if sql]:
                    try:
                        with _conn.begin() as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            self._logger.debug("executed the sql '%s'.", sql)
                    except:
                        self._logger.warning("an error occurred when executing the sql '%s'.", sql)
                        raise
                try:
                    with _conn.begin() as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE chronovoyage_periods SET has_come = TRUE WHERE id = ?", (inserted_period_id,))
                        self._logger.debug("updated the period which id is %d.", inserted_period_id)
                except:
                    self._logger.warning("an error occurred when updating the period '%s'.", period.period_name)
                    raise
                self._logger.info("the period '%s' has come.", period.period_name)
