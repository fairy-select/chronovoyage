import pytest

from chronovoyage.internal.database.connection import ConnectionInfo, DatabaseConnector
from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.internal.type.enum import DatabaseVendorEnum


class TestConnection:
    def test_connect_to_mariadb(self, database_helper) -> None:
        cnx = database_helper.get_connection(DatabaseVendorEnum.MARIADB)
        assert cnx is not None

    def test_connect_to_unknown(self) -> None:
        # given
        connection_info = ConnectionInfo(host="", port=0, user="", password="", database="")
        # when/then
        with pytest.raises(DatabaseUnknownVendorError):
            # noinspection PyTypeChecker
            DatabaseConnector().get_connection("unknown", connection_info)
