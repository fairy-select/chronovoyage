from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from chronovoyage.internal.exception.database import DatabaseUnknownVendorError
from chronovoyage.logger import get_default_logger

if TYPE_CHECKING:
    from logging import Logger

    from chronovoyage.type.enum import DatabaseVendorEnum


@dataclass(frozen=True)
class ConnectionInfo:
    host: str
    port: int
    user: str
    password: str
    database: str


class DatabaseConnector:
    def __init__(self, *, logger: Logger | None = None) -> None:
        self._logger = logger if logger is not None else get_default_logger()

    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendorEnum, connection_info: ConnectionInfo):
        if vendor == "mariadb":
            from chronovoyage.database import mariadb

            return mariadb.connect(connection_info, logger=self._logger)

        raise DatabaseUnknownVendorError
