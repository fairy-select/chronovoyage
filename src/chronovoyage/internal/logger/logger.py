from __future__ import annotations

import logging
import logging.config
import os.path
from typing import ClassVar

import yaml

from chronovoyage import SRC_ROOT


class BaseAppLogger:
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


class AppLogger(BaseAppLogger):
    pass


class AppLoggerDebug(BaseAppLogger):
    pass


class AppLoggerFactory:
    __verbose = False

    @classmethod
    def set_verbose(cls, *, verbose: bool) -> None:
        cls.__verbose = verbose

    @classmethod
    def get_instance(cls) -> AppLoggerDebug | AppLogger:
        if cls.__verbose:
            return AppLoggerDebug()
        return AppLogger()


def get_default_logger() -> AppLogger:
    return AppLoggerFactory.get_instance()


def __setup_logging():
    with open(os.path.join(SRC_ROOT, "logging.yaml")) as f:
        config_ = f.read()
    logging.config.dictConfig(yaml.load(config_, Loader=yaml.SafeLoader))


__setup_logging()
