from typing import Literal, overload

from chronovoyage.internal.database.mariadb_ import MariadbDatabaseConnection
from chronovoyage.internal.interface.database import IDatabaseConnection
from chronovoyage.internal.logger.logger import AppLogger
from chronovoyage.internal.type.database import ConnectionInfo
from chronovoyage.internal.type.enum import DatabaseVendorEnum

class DatabaseConnector:
    _logger: AppLogger

    def __init__(self, *, logger: AppLogger) -> None: ...
    @overload
    def get_connection(
        self, vendor: Literal[DatabaseVendorEnum.MARIADB], connection_info: ConnectionInfo
    ) -> MariadbDatabaseConnection: ...
    @overload
    def get_connection(self, vendor: DatabaseVendorEnum, connection_info: ConnectionInfo) -> IDatabaseConnection: ...
