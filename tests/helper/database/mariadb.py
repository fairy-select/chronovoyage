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
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND SUBSTR(TABLE_NAME, 0, 13) != 'chronovoyage_'",
        (database,),
    )
    return {table_name for (table_name,) in cursor.fetchall()}


def truncate_mariadb_test_db(database: str) -> None:
    with get_default_mariadb_connection() as wrapper:
        cursor = wrapper.cursor()
        for table_name in mariadb_get_tables(database, cursor):
            if not re.match(r"\w+", table_name):  # pragma: no cover
                pytest.fail(f"{table_name} is an invalid table name.")
            cursor.execute("DROP TABLE " + table_name)


def get_default_mariadb_connection():
    return DatabaseConnector().get_connection(DatabaseVendorEnum.MARIADB, default_mariadb_connection_info())
