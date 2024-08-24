import sys
from dataclasses import dataclass
from typing import Literal

from chronovoyage.exception.database import DatabaseUnknownVendorError

DatabaseVendor = Literal["mariadb"]


@dataclass(frozen=True)
class ConnectionInfo:
    user: str
    password: str
    host: str
    port: int

class DatabaseConnector:
    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendor, connection_info: ConnectionInfo):
        if vendor == "mariadb":
            import mariadb
            try:
                conn = mariadb.connect(
                    user=connection_info.user,
                    password=connection_info.password,
                    host=connection_info.host,
                    port=connection_info.port,
                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            return conn

        raise DatabaseUnknownVendorError()
