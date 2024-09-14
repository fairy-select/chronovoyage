from __future__ import annotations

import json
import os
import string
from typing import TYPE_CHECKING, Any

from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.type.config import MigratePeriodCreateParam
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

    def create_migrate_period(self, to_directory: str, params: MigratePeriodCreateParam) -> None:
        self._validate_directory(to_directory)
        directory_name = string.Template("${period_name}_${language}_${description}").safe_substitute(period_name=params.period_name, language=params.language.value, description=params.description)
        os.makedirs(directory_name)
        for file in ("go.sql", "return.sql"):
            with open(os.path.join(directory_name, file), "w") as _:
                # create empty file
                pass

    # noinspection PyMethodMayBeStatic
    def _validate_directory(self, directory: str) -> None:
        # valid means config can be created
        MigrateDomainConfigFactory.create_from_directory(directory)
