from logging import Logger

from chronovoyage.internal.config import MigrateDomainConfig
from chronovoyage.internal.database.connection import DatabaseConnector


class MigrateUsecase:
    def __init__(self, *, config: MigrateDomainConfig, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def migrate(self):
        with DatabaseConnector().get_connection(self._config.vendor, self._config.connection_info) as _conn:
            for sql_path in [period.go_sql_path for period in self._config.periods]:
                with open(sql_path) as f:
                    file_content = f.read()
                for sql in [sql.strip() for sql in file_content.strip().split(";") if sql]:
                    try:
                        with _conn.begin() as conn:
                            cursor = conn.cursor()
                            cursor.execute(sql)
                    except:
                        self._logger.warning("an error occurred when executing '%s'.", sql)
                        raise
