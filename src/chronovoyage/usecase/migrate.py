from logging import Logger

from chronovoyage.database.connection import DatabaseConnector
from chronovoyage.config.migrate import MigrateDomainConfig


class MigrateUsecase:
    def __init__(self, *, config: MigrateDomainConfig, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def migrate(self):
        with DatabaseConnector().get_connection(self._config.vendor, self._config.connection_info) as _conn:
            for sql_path in [period.go_sql_path for period in self._config.periods]:
                for sql in [sql.strip() for sql in open(sql_path).read().strip().split(";") if sql]:
                    try:
                        with _conn.begin() as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql)
                    except:
                        self._logger.warning(f"an error occurred when executing '{sql}'.")
                        raise
