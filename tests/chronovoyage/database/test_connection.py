import pytest

from chronovoyage.internal.database.connection import ConnectionInfo, DatabaseConnector
from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.internal.type.enum import DatabaseVendorEnum
from helper import DEFAULT_TEST_ENV


class TestConnection:
    def test_connect_to_mariadb(self) -> None:
        # given
        connection_info = ConnectionInfo(
                host="127.0.0.1",
                port=3307,
                user=DEFAULT_TEST_ENV["MARIADB_USER"],
                password=DEFAULT_TEST_ENV["MARIADB_PASSWORD"],
                database=DEFAULT_TEST_ENV["MARIADB_DATABASE"],
        )
        # when
        conn = DatabaseConnector().get_connection(DatabaseVendorEnum.MARIADB, connection_info)
        # then
        assert conn is not None

    def test_connect_to_unknown(self) -> None:
        # given
        connection_info = ConnectionInfo(host="", port=0, user="", password="", database="")
        # when/then
        with pytest.raises(DatabaseUnknownVendorError):
            # noinspection PyTypeChecker
            DatabaseConnector().get_connection("unknown", connection_info)
