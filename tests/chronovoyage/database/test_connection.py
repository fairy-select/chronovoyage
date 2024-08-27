import pytest
from helper import default_mariadb_connection_info

from chronovoyage.internal.database.connection import ConnectionInfo, DatabaseConnector
from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum


class TestConnection:
    def test_connect_to_mariadb(self) -> None:
        # given
        connection_info = default_mariadb_connection_info()
        # when
        conn = DatabaseConnector(logger=get_default_logger()).get_connection(DatabaseVendorEnum.MARIADB, connection_info)
        # then
        assert conn is not None

    def test_connect_to_unknown(self) -> None:
        # given
        connection_info = ConnectionInfo(host="", port=0, user="", password="", database="")
        # when/then
        with pytest.raises(DatabaseUnknownVendorError):
            # noinspection PyTypeChecker
            # vendor in get_connection
            DatabaseConnector(logger=get_default_logger()).get_connection("unknown", connection_info)
