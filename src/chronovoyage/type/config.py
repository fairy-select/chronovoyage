from typing import TypedDict


class _MigrateConfigJsonConnectionInfo(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str


class MigrateConfigJson(TypedDict):
    vendor: str
    connection_info: _MigrateConfigJsonConnectionInfo
