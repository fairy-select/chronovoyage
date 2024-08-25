import re

import pytest
from helper import DEFAULT_TEST_ENV, default_mariadb_connection_info

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.type.enum import DatabaseVendorEnum


def truncate_mariadb_test_db() -> None:
    with DatabaseConnector().get_connection(DatabaseVendorEnum.MARIADB, default_mariadb_connection_info()) as wrapper:
        # noinspection PyProtectedMember
        cursor = wrapper._conn.cursor()  # noqa: SLF001
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = ?",
            (DEFAULT_TEST_ENV["MARIADB_DATABASE"],),
        )
        for (table_name,) in cursor.fetchall():
            table_name: str
            if not re.match(r"\w+", table_name):  # pragma: no cover
                pytest.fail(f"{table_name} is an invalid table name.")
            cursor.execute("DROP TABLE " + table_name)
