from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionInfo:
    host: str
    port: int
    user: str
    password: str
    database: str
