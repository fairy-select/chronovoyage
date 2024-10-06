from __future__ import annotations

import logging
from logging import StreamHandler, getLogger
from typing import ClassVar, Mapping

import click

from chronovoyage.internal.type.dict import LogStyle


class ClickEchoHandler(StreamHandler):
    __style: ClassVar[Mapping[int, LogStyle]] = {
        logging.DEBUG: LogStyle(fg="green"),
        logging.INFO: LogStyle(fg="blue"),
        logging.WARNING: LogStyle(fg="yellow"),
        logging.ERROR: LogStyle(fg="red"),
    }

    def emit(self, record):
        message = self.formatter.format(record)
        style = self.__style.get(record.levelno, LogStyle())
        click.secho(message, **style)


class AppLogger:
    __available_log_level: ClassVar[set[str]] = {"debug", "info", "warning", "error"}
    __logger = None

    def __init__(self) -> None:
        if self.__logger is None:
            self.__logger = getLogger(self.__class__.__name__)
            cli_log = ClickEchoHandler()
            cli_log.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
            self.__logger.addHandler(cli_log)
        self._logger = self.__logger

    def __getattr__(self, item):
        if item in self.__available_log_level:
            return getattr(self._logger, item)
        return getattr(self, item)


def get_default_logger() -> AppLogger:
    return AppLogger()
