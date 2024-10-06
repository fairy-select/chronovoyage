import pytest
from support import default_mariadb_connection_info

from chronovoyage.internal.database.connection import DatabaseConnector
from chronovoyage.internal.logger.logger import get_default_logger
from chronovoyage.internal.type.database import ConnectionInfo
from chronovoyage.internal.type.enum import DatabaseVendorEnum


class TestConnection:
    def test_connect_to_mariadb(self) -> None:
        # given
        connection_info = default_mariadb_connection_info()
        # when
        conn = DatabaseConnector(logger=get_default_logger()).get_connection(
            DatabaseVendorEnum.MARIADB, connection_info
        )
        # then
        assert conn is not None

    def test_connect_to_unknown(self) -> None:
        # given
        connection_info = ConnectionInfo(host=..., port=..., user=..., password=..., database=...)  # type: ignore[arg-type]
        # when/then
        with pytest.raises(ValueError, match=r"Given database vendor is invalid"):
            DatabaseConnector(logger=get_default_logger()).get_connection(
                DatabaseVendorEnum("unknown"), connection_info
            )
