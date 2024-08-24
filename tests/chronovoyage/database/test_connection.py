import pytest

from chronovoyage.database.connection import DatabaseConnector, ConnectionInfo
from chronovoyage.exception.database import DatabaseUnknownVendorError


class TestConnection:
    def test_connect_to_mariadb(self, database_helper) -> None:
        cnx = database_helper.get_connection('mariadb')
        assert cnx is not None

    def test_connect_to_unknown(self) -> None:
        # given
        connection_info = ConnectionInfo(user="", password="", host="", port=0)
        # when/then
        with pytest.raises(DatabaseUnknownVendorError):
            # noinspection PyTypeChecker
            DatabaseConnector().get_connection('unknown', connection_info)
