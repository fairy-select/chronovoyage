from __future__ import annotations

from typing import TYPE_CHECKING

from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.internal.interface.database import IDatabaseConnection
    from chronovoyage.internal.type.database import ConnectionInfo


class DatabaseConnector:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger

    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendorEnum, connection_info: ConnectionInfo) -> IDatabaseConnection:
        if vendor == DatabaseVendorEnum.MARIADB:
            from chronovoyage.internal.database import _mariadb

            return _mariadb.connect(connection_info, logger=self._logger)

        raise DatabaseUnknownVendorError
