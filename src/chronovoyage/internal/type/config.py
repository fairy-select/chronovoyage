from dataclasses import dataclass
from typing import TypedDict

from chronovoyage.internal.type.enum import MigratePeriodLanguageEnum


class _MigrateConfigJsonConnectionInfo(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str


class MigrateConfigJson(TypedDict):
    vendor: str
    connection_info: _MigrateConfigJsonConnectionInfo


@dataclass(frozen=True)
class MigratePeriodCreateParam:
    period_name: str
    language: MigratePeriodLanguageEnum
    description: str
