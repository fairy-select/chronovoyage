import sys
from logging import Logger

import mariadb

from chronovoyage.internal.database.connection import ConnectionInfo
from chronovoyage.internal.interface.database import IDatabaseConnection, PCanHandleTransaction


def connect(connection_info: ConnectionInfo, *, logger: Logger):
    try:
        conn = mariadb.connect(
            host=connection_info.host,
            port=connection_info.port,
            user=connection_info.user,
            password=connection_info.password,
            database=connection_info.database,
        )
    except mariadb.Error:
        logger.exception("Error connecting to MariaDB Platform")
        sys.exit(1)

    return MariadbDatabaseConnection(conn)


class MariadbDatabaseTransaction:
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def __enter__(self) -> mariadb.Connection:
        self._conn.begin()
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()


class MariadbDatabaseConnectionWrapper(PCanHandleTransaction):
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def begin(self) -> MariadbDatabaseTransaction:
        return MariadbDatabaseTransaction(self._conn)

    def cursor(self) -> mariadb.cursors.Cursor:
        return self._conn.cursor()


class MariadbDatabaseConnection(IDatabaseConnection):
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def __enter__(self) -> MariadbDatabaseConnectionWrapper:
        return MariadbDatabaseConnectionWrapper(self._conn)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._conn.close()
