from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from logging import Logger

config_templates: dict[DatabaseVendorEnum, dict[str, Any]] = {
    DatabaseVendorEnum.MARIADB: {
        "$schema": "https://raw.githubusercontent.com/noritakaIzumi/chronovoyage/main/schema/config.schema.json",
        "vendor": "mariadb",
        "connection_info": {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "mariadb",
            "password": "password",
            "database": "test",
        },
    },
}


class InitUsecase:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger

    def create_files(self, *, vendor: DatabaseVendorEnum, to_directory: str) -> None:
        os.makedirs(to_directory, exist_ok=True)
        self._logger.debug("created directory: %s", to_directory)
        with open(os.path.join(to_directory, "config.json"), "w") as f:
            f.write(json.dumps(config_templates[vendor], indent=2))
            f.write("\n")
        self._logger.info("created file: config.json")

    def create_migrate_period(self, directory_name: str) -> None:
        pass
