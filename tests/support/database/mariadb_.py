from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest
from support import DEFAULT_TEST_ENV, default_mariadb_connection_info

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from mariadb import Cursor


class SupportMariadb:
    @staticmethod
    def get_default_mariadb_connection():
        return DatabaseConnector(logger=get_default_logger()).get_connection(
            DatabaseVendorEnum.MARIADB, default_mariadb_connection_info()
        )

    @staticmethod
    def _mariadb_get_tables(cursor: Cursor) -> set[str]:
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) != 'chronovoyage_'",
            (DEFAULT_TEST_ENV["MARIADB_DATABASE"],),
        )
        return {table_name for (table_name,) in cursor.fetchall()}

    @staticmethod
    def _mariadb_get_system_tables(cursor: Cursor) -> set[str]:
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) = 'chronovoyage_'",
            (DEFAULT_TEST_ENV["MARIADB_DATABASE"],),
        )
        return {table_name for (table_name,) in cursor.fetchall()}

    @classmethod
    def get_tables(cls):
        with cls.get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            return cls._mariadb_get_tables(cursor)

    @classmethod
    def all_periods_have_come(cls) -> bool:
        with cls.get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT has_come FROM chronovoyage_periods")
            return {has_come for (has_come,) in cursor.fetchall()} == {True}

    @classmethod
    def assert_rows_and_sql(cls, want_rows: list[tuple[Any, ...]], sql: str) -> None:
        with cls.get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if cursor.rowcount != len(want_rows):
                pytest.fail(f"件数が異なる (want: {len(want_rows)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_rows[i], f"row {i}"

    @classmethod
    def truncate_mariadb_test_db(cls) -> None:
        with cls.get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            for table in cls._mariadb_get_tables(cursor):
                if not re.match(r"\w+", table):  # pragma: no cover
                    pytest.fail(f"{table} is an invalid table name.")
                cursor.execute("DROP TABLE " + table)
            for system_table in cls._mariadb_get_system_tables(cursor):
                if not re.match(r"\w+", system_table):  # pragma: no cover
                    pytest.fail(f"{system_table} is an invalid table name.")
                cursor.execute("DROP TABLE " + system_table)
