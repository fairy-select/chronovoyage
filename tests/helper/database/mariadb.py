from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from helper import default_mariadb_connection_info

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from mariadb import Cursor


def mariadb_get_tables(database: str, cursor: Cursor) -> set[str]:
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) != 'chronovoyage_'",
        (database,),
    )
    return {table_name for (table_name,) in cursor.fetchall()}


def mariadb_get_system_tables(database: str, cursor: Cursor) -> set[str]:
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME FROM 1 FOR 13) = 'chronovoyage_'",
        (database,),
    )
    return {table_name for (table_name,) in cursor.fetchall()}


def truncate_mariadb_test_db(database: str) -> None:
    with get_default_mariadb_connection() as wrapper:
        cursor = wrapper.cursor()
        for table in mariadb_get_tables(database, cursor):
            if not re.match(r"\w+", table):  # pragma: no cover
                pytest.fail(f"{table} is an invalid table name.")
            cursor.execute("DROP TABLE " + table)
        for system_table in mariadb_get_system_tables(database, cursor):
            if not re.match(r"\w+", system_table):  # pragma: no cover
                pytest.fail(f"{system_table} is an invalid table name.")
            cursor.execute("TRUNCATE TABLE " + system_table)


def get_default_mariadb_connection():
    return DatabaseConnector().get_connection(DatabaseVendorEnum.MARIADB, default_mariadb_connection_info())
