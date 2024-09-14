import json
import os
from logging import Logger


class InitUsecase:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger

    def create_files(self, *, to_directory: str) -> None:
        os.makedirs(to_directory, exist_ok=True)
        config = {
            "$schema": "https://raw.githubusercontent.com/noritakaIzumi/chronovoyage/main/schema/config.schema.json",
            "vendor": "mariadb",
            "connection_info": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "mariadb",
                "password": "password",
                "database": "test"
            },
        }
        with open(os.path.join(to_directory, "config.json"), "w") as f:
            f.write(json.dumps(config, indent=2))
            f.write("\n")
