from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Generator, Iterable

import mariadb

from chronovoyage.internal.interface.database import (
    IDatabaseConnection,
    IDatabaseConnectionWrapper,
)

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod
    from chronovoyage.internal.logger.logger import AppLogger
    from chronovoyage.internal.type.database import ConnectionInfo


def connect(connection_info: ConnectionInfo, *, logger: AppLogger):
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

    def begin(self) -> MariadbDatabaseTransaction:
        return MariadbDatabaseTransaction(self._conn)

    def find_period_id(self, period: MigratePeriod) -> int | None:
        with self.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT id FROM chronovoyage_periods WHERE period_name = %s", (period.period_name,))
            row = cursor.fetchone()
            if row is None:
                return None
            (_id,) = row
            return _id

    def add_period(self, period: MigratePeriod) -> int:
        with self.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
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
        with self.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

    def mark_period_as_come(self, inserted_period_id: int) -> None:
        with self.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("UPDATE chronovoyage_periods SET has_come = TRUE WHERE id = ?", (inserted_period_id,))

    def mark_period_as_not_come(self, inserted_period_id: int) -> None:
        with self.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("UPDATE chronovoyage_periods SET has_come = FALSE WHERE id = ?", (inserted_period_id,))

    def get_current_period(self) -> str | None:
        with self.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT period_name FROM chronovoyage_periods WHERE has_come IS TRUE ORDER BY id DESC")
            row = cursor.fetchone()
            if row is None:
                return None
            (period_name,) = row
            return period_name

    def create_if_not_exists_system_table(self) -> bool:
        with self.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND TABLE_NAME = 'chronovoyage_periods'",
                (conn.database,),
            )
            if cursor.fetchone() is not None:
                return False
            cursor.execute(
                """
CREATE TABLE chronovoyage_periods
(
    `id`          INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `period_name` VARCHAR(14)   NOT NULL UNIQUE COMMENT 'バージョン名 (%Y%m%d%H%M%S)',
    `language`    VARCHAR(3)    NOT NULL COMMENT '言語種別 (ddl/dml)',
    `description` VARCHAR(4096) NOT NULL COMMENT '説明',
    `has_come`    BOOLEAN       NOT NULL DEFAULT FALSE COMMENT 'TRUE: 反映済みである, FALSE: 未反映・ロールバック済みである',
    `is_verified` BOOLEAN       NOT NULL DEFAULT FALSE COMMENT 'go.sql と return.sql のデータ整合性が検証済みである'
) COMMENT 'マイグレーションバージョン管理';
""".strip()
            )
            return True

    def system_table_exists(self) -> bool:
        with self.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND TABLE_NAME = 'chronovoyage_periods'",
                (conn.database,),
            )
            return cursor.fetchone() is not None

    def get_all_come_periods(self, *, reverse: bool) -> Iterable[tuple[int, str]]:
        with self.begin() as conn:
            cursor = conn.cursor()
            if reverse:
                # noinspection SqlResolve
                cursor.execute(
                    "SELECT id, period_name FROM chronovoyage_periods WHERE has_come IS TRUE ORDER BY id DESC"
                )
            else:
                # noinspection SqlResolve
                cursor.execute("SELECT id, period_name FROM chronovoyage_periods WHERE has_come IS TRUE ORDER BY id")
            rows = cursor.fetchall()
        for row in rows:
            (period_id, period_name) = row
            yield period_id, period_name


class MariadbDatabaseConnection(IDatabaseConnection):
    def __init__(self, _conn: mariadb.Connection) -> None:
        self._conn = _conn

    def __enter__(self) -> MariadbDatabaseConnectionWrapper:
        return MariadbDatabaseConnectionWrapper(self._conn)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._conn.close()
