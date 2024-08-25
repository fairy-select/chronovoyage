from logging import Logger

from chronovoyage.database.connection import DatabaseConnector
from chronovoyage.config.migrate import MigrateDomainConfig


class MigrateUsecase:
    def __init__(self, *, config: MigrateDomainConfig, logger: Logger) -> None:
        self._config = config
        self._logger = logger

    def _connect_database(self):
        self._logger.debug("データベースに接続")
        return DatabaseConnector().get_connection("mariadb", self._config.connection_info)

    def マイグレーションを実行する(self):
        self._logger.info("マイグレーションを実行する")
        cnx = self._connect_database()
