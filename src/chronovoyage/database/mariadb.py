import sys
from logging import Logger

from chronovoyage.database.connection import ConnectionInfo


def connect(connection_info: ConnectionInfo, *, logger: Logger):
    import mariadb

    try:
        conn = mariadb.connect(
            host=connection_info.host,
            port=connection_info.port,
            user=connection_info.user,
            password=connection_info.password,
        )
    except mariadb.Error:
        logger.exception("Error connecting to MariaDB Platform")
        sys.exit(1)

    class MariadbDatabaseTransaction:
        def __init__(self, _conn: mariadb.Connection) -> None:
            self._conn = conn

        def __enter__(self) -> mariadb.Connection:
            self._conn.begin()
            return self._conn

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            if exc_type is None:
                self._conn.commit()
            else:
                self._conn.rollback()

    class MariadbDatabaseConnectionWrapper:
        def __init__(self, _conn: mariadb.Connection) -> None:
            self._conn = conn

        def begin(self) -> MariadbDatabaseTransaction:
            return MariadbDatabaseTransaction(self._conn)

    class MariadbDatabaseConnection:
        def __init__(self, _conn: mariadb.Connection) -> None:
            self._conn = conn

        def __enter__(self) -> MariadbDatabaseConnectionWrapper:
            return MariadbDatabaseConnectionWrapper(self._conn)

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            self._conn.close()

    return MariadbDatabaseConnection(conn)
