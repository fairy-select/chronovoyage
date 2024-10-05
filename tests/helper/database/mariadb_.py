from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest
from helper import DEFAULT_TEST_ENV, default_mariadb_connection_info

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from mariadb import Cursor


def mariadb_get_tables(cursor: Cursor) -> set[str]:
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) != 'chronovoyage_'",
        (DEFAULT_TEST_ENV["MARIADB_DATABASE"],),
    )
    return {table_name for (table_name,) in cursor.fetchall()}


def mariadb_get_system_tables(cursor: Cursor) -> set[str]:
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) = 'chronovoyage_'",
        (DEFAULT_TEST_ENV["MARIADB_DATABASE"],),
    )
    return {table_name for (table_name,) in cursor.fetchall()}


def truncate_mariadb_test_db() -> None:
    with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
        cursor = conn.cursor()
        for table in mariadb_get_tables(cursor):
            if not re.match(r"\w+", table):  # pragma: no cover
                pytest.fail(f"{table} is an invalid table name.")
            cursor.execute("DROP TABLE " + table)
        for system_table in mariadb_get_system_tables(cursor):
            if not re.match(r"\w+", system_table):  # pragma: no cover
                pytest.fail(f"{system_table} is an invalid table name.")
            cursor.execute("DROP TABLE " + system_table)


def get_default_mariadb_connection():
    return DatabaseConnector(logger=get_default_logger()).get_connection(
        DatabaseVendorEnum.MARIADB, default_mariadb_connection_info()
    )


class SupportMariadb:
    @staticmethod
    def get_tables():
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            return mariadb_get_tables(cursor)

    @staticmethod
    def assert_rows_and_sql(want_rows: list[tuple[Any, ...]], sql: str) -> None:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if cursor.rowcount != len(want_rows):
                pytest.fail(f"件数が異なる (want: {len(want_rows)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_rows[i], f"row {i}"
