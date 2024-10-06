from __future__ import annotations

import logging
import logging.config
import os.path
from typing import ClassVar

import yaml

from chronovoyage import SRC_ROOT


class AppLogger:
    __available_log_level: ClassVar[set[str]] = {"debug", "info", "warning", "error"}
    __logger = None

    def __init__(self) -> None:
        if self.__logger is None:
            self.__logger = logging.getLogger(self.__class__.__name__)
        self._logger = self.__logger

    def __getattr__(self, item):
        if item in self.__available_log_level:
            return getattr(self._logger, item)
        return getattr(self, item)


def get_default_logger() -> AppLogger:
    return AppLogger()


logging.config.dictConfig(yaml.load(open(os.path.join(SRC_ROOT, "logging.yaml")).read(), Loader=yaml.SafeLoader))
