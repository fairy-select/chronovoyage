import pytest
from helper import DEFAULT_TEST_ENV

from chronovoyage.database.connection import ConnectionInfo, DatabaseConnector
from chronovoyage.type.enum import DatabaseVendorEnum


class DatabaseHelper:
    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendorEnum):
        database_connector = DatabaseConnector()
        if vendor == "mariadb":
            connection_info = ConnectionInfo(
                host="127.0.0.1",
                port=3307,
                user=DEFAULT_TEST_ENV["MARIADB_USER"],
                password=DEFAULT_TEST_ENV["MARIADB_PASSWORD"],
            )
            return database_connector.get_connection(vendor, connection_info)

        pytest.fail(f"{vendor} is an unknown vendor.")
