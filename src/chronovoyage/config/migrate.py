import json
import os
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

from chronovoyage.database.connection import ConnectionInfo
from chronovoyage.exception.config import MigrateConfigVersionNameInvalidError, MigrateConfigSqlMissingError


@dataclass
class MigratePeriod:
    period: str
    language: str
    description: str
    go_sql_path: str
    return_sql_path: str


@dataclass
class MigrateDomainConfig:
    vendor: str
    connection_info: ConnectionInfo
    periods: List[MigratePeriod]


class MigrateDomainConfigFactory:
    # noinspection PyMethodMayBeStatic
    def create_from_directory(self, directory: str) -> MigrateDomainConfig:
        vendor, connection_info = self._parse_config(directory)
        periods = self._parse_sql(directory)
        return MigrateDomainConfig(vendor=vendor, connection_info=connection_info, periods=periods)

    # noinspection PyMethodMayBeStatic
    def _parse_config(self, directory: str) -> Tuple[str, ConnectionInfo]:
        config: Dict[str, Any] = json.loads(open(f"{directory}/config.json").read())
        vendor = str(config.get('vendor'))
        connection_info = ConnectionInfo(
            user=config.get('user'),
            password=config.get("password"),
            host=config.get("host"),
            port=config.get("port"),
        )
        return vendor, connection_info

    # noinspection PyMethodMayBeStatic
    def _parse_sql(self, directory: str) -> List[MigratePeriod]:
        os.chdir(directory)

        sqls: List[MigratePeriod] = []
        for _dir in filter(lambda f: os.path.isdir(f), os.listdir()):
            matched = re.match(r"(?P<period>\d{4}\d{2}\d{2}\d{6})_(?P<language>(ddl|dml))_(?P<description>\w+)", _dir)
            if not matched:
                # TODO: test
                raise MigrateConfigVersionNameInvalidError(_dir)
            if not {"go.sql", "return.sql"} <= set(os.listdir(_dir)):
                # TODO: test
                raise MigrateConfigSqlMissingError(_dir)
            _dir_realpath = os.path.realpath(_dir)
            sqls.append(MigratePeriod(
                period=matched.group("period"),
                language=matched.group("language"),
                description=matched.group("description"),
                go_sql_path=f"{_dir_realpath}/go.sql",
                return_sql_path=f"{_dir_realpath}/return.sql",
            ))

        # TODO: sort by period
        return sqls
