from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from chronovoyage.internal.interface.database import IDatabaseConnection
    from chronovoyage.internal.logger.logger import AppLogger
    from chronovoyage.internal.type.database import ConnectionInfo


class DatabaseConnector:
    def __init__(self, *, logger: AppLogger) -> None:
        self._logger = logger

    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendorEnum, connection_info: ConnectionInfo) -> IDatabaseConnection:
        if vendor == DatabaseVendorEnum.MARIADB:
            from chronovoyage.internal.database import mariadb_

            return mariadb_.connect(connection_info, logger=self._logger)

        raise DatabaseUnknownVendorError
