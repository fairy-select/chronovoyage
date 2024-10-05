from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.type.database import ConnectionInfo
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from chronovoyage.internal.type.config import MigrateConfigJson


@dataclass(frozen=True)
class MigratePeriod:
    period_name: str
    language: str
    description: str
    go_sql_path: str
    return_sql_path: str

    def __lt__(self, other: MigratePeriod) -> bool:
        """時代の並び替えは時代名昇順"""
        return self.period_name < other.period_name


@dataclass(frozen=True)
class MigrateConfig:
    vendor: DatabaseVendorEnum
    connection_info: ConnectionInfo
    periods: list[MigratePeriod]


class MigrateConfigFactory:
    @classmethod
    def create_from_directory(cls, directory: str) -> MigrateConfig:
        vendor, connection_info = cls._parse_config(directory)
        periods = cls._parse_sql(directory)
        return MigrateConfig(vendor=vendor, connection_info=connection_info, periods=periods)

    @classmethod
    def _parse_config(cls, directory: str) -> tuple[DatabaseVendorEnum, ConnectionInfo]:
        with open(f"{directory}/config.json") as f:
            config: MigrateConfigJson = json.loads(f.read())
        vendor = DatabaseVendorEnum(config["vendor"])
        connection_info = ConnectionInfo(
            host=config["connection_info"]["host"],
            port=config["connection_info"]["port"],
            user=config["connection_info"]["user"],
            password=config["connection_info"]["password"],
            database=config["connection_info"]["database"],
        )
        return vendor, connection_info

    @classmethod
    def _parse_sql(cls, directory: str) -> list[MigratePeriod]:
        os.chdir(directory)

        periods: list[MigratePeriod] = []
        for _dir in filter(lambda f: os.path.isdir(f), os.listdir()):
            matched = re.match(
                r"(?P<period_name>\d{4}\d{2}\d{2}\d{6})_(?P<language>(ddl|dml))_(?P<description>\w+)", _dir
            )
            if not matched:
                raise MigrateConfigVersionNameInvalidError(_dir)
            _files = os.listdir(_dir)
            if "go.sql" not in _files:
                raise MigrateConfigGoSqlMissingError(_dir)
            if "return.sql" not in _files:
                raise MigrateConfigReturnSqlMissingError(_dir)
            _dir_realpath = os.path.realpath(_dir)
            periods.append(
                MigratePeriod(
                    period_name=matched.group("period_name"),
                    language=matched.group("language"),
                    description=matched.group("description"),
                    go_sql_path=f"{_dir_realpath}/go.sql",
                    return_sql_path=f"{_dir_realpath}/return.sql",
                )
            )

        return sorted(periods)
