from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from chronovoyage.exception.database import DatabaseUnknownVendorError
from chronovoyage.logger import get_default_logger
from chronovoyage.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from logging import Logger



@dataclass(frozen=True)
class ConnectionInfo:
    user: str
    password: str
    host: str
    port: int


class DatabaseConnector:
    def __init__(self, *, logger: Logger | None = None) -> None:
        self._logger = logger if logger is not None else get_default_logger()

    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendorEnum, connection_info: ConnectionInfo):
        if vendor == "mariadb":
            import mariadb

            try:
                conn = mariadb.connect(
                    user=connection_info.user,
                    password=connection_info.password,
                    host=connection_info.host,
                    port=connection_info.port,
                )
            except mariadb.Error:
                self._logger.exception("Error connecting to MariaDB Platform")
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

        raise DatabaseUnknownVendorError
