from __future__ import annotations

import logging
import logging.config
import os.path
from typing import ClassVar

import yaml
from typing_extensions import Self

from chronovoyage import SRC_ROOT


class AppLogger:
    __available_log_level: ClassVar[set[str]] = {"debug", "info", "warning", "error"}
    __logger = None
    __verbose = False

    @classmethod
    def set_verbose(cls, *, verbose: bool) -> None:
        cls.__verbose = verbose

    @classmethod
    def get_instance(cls) -> Self:
        return cls(verbose=cls.__verbose)

    def __init__(self, *, verbose: bool) -> None:
        logger_name = self.__class__.__name__
        if verbose:
            logger_name += "-debug"
        if self.__logger is None:
            self.__logger = logging.getLogger(logger_name)
        self._logger = self.__logger

    def __getattr__(self, item):
        if item in self.__available_log_level:
            return getattr(self._logger, item)
        return getattr(self, item)


def get_default_logger() -> AppLogger:
    return AppLogger.get_instance()


def __setup_logging():
    with open(os.path.join(SRC_ROOT, "logging.yaml")) as f:
        config_ = f.read()
    logging.config.dictConfig(yaml.load(config_, Loader=yaml.SafeLoader))


__setup_logging()
