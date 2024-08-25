from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from chronovoyage.database.connection import ConnectionInfo
from chronovoyage.exception.config import MigrateConfigSqlMissingError, MigrateConfigVersionNameInvalidError, \
    MigrateConfigGoSqlMissingError, MigrateConfigReturnSqlMissingError
from chronovoyage.type.config import MigrateConfigJson
from chronovoyage.type.enum import DatabaseVendorEnum


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
class MigrateDomainConfig:
    vendor: DatabaseVendorEnum
    connection_info: ConnectionInfo
    periods: list[MigratePeriod]


class MigrateDomainConfigFactory:
    # noinspection PyMethodMayBeStatic
    def create_from_directory(self, directory: str) -> MigrateDomainConfig:
        vendor, connection_info = self._parse_config(directory)
        periods = self._parse_sql(directory)
        return MigrateDomainConfig(vendor=vendor, connection_info=connection_info, periods=periods)

    # noinspection PyMethodMayBeStatic
    def _parse_config(self, directory: str) -> tuple[DatabaseVendorEnum, ConnectionInfo]:
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

    # noinspection PyMethodMayBeStatic
    def _parse_sql(self, directory: str) -> list[MigratePeriod]:
        os.chdir(directory)

        periods: list[MigratePeriod] = []
        for _dir in filter(lambda f: os.path.isdir(f), os.listdir()):
            matched = re.match(r"(?P<period_name>\d{4}\d{2}\d{2}\d{6})_(?P<language>(ddl|dml))_(?P<description>\w+)", _dir)
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
