from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Generator

import mariadb

from chronovoyage.internal.interface.database import (
    IDatabaseConnection,
    IDatabaseConnectionWrapper,
)

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.internal.config import MigratePeriod
    from chronovoyage.internal.type.database import ConnectionInfo


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


class MariadbDatabaseConnectionWrapper(IDatabaseConnectionWrapper):
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def _begin(self) -> MariadbDatabaseTransaction:
        return MariadbDatabaseTransaction(self._conn)

    def cursor(self) -> mariadb.cursors.Cursor:
        return self._conn.cursor()

    def add_period(self, period: MigratePeriod) -> int:
        with self._begin() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chronovoyage_periods (period_name, language, description) VALUES (?, ?, ?)",
                (period.period_name, period.language, period.description),
            )
            return cursor.lastrowid

    def get_sqls(self, filepath: str) -> Generator[str, Any, None]:
        with open(filepath) as f:
            file_content = f.read()
        return (sql.strip() for sql in file_content.strip().split(";") if sql)

    def execute_sql(self, sql: str) -> None:
        with self._begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

    def mark_period_as_come(self, inserted_period_id: int) -> None:
        with self._begin() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE chronovoyage_periods SET has_come = TRUE WHERE id = ?", (inserted_period_id,))

    def get_current_period(self) -> str | None:
        with self._begin() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT period_name FROM chronovoyage_periods WHERE has_come IS TRUE ORDER BY id DESC")
            row = cursor.fetchone()
            if row is None:
                return None
            (period_name,) = row
            return period_name


class MariadbDatabaseConnection(IDatabaseConnection):
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def __enter__(self) -> MariadbDatabaseConnectionWrapper:
        return MariadbDatabaseConnectionWrapper(self._conn)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._conn.close()
