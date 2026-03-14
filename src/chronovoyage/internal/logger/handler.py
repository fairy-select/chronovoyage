from __future__ import annotations

import logging
from logging import StreamHandler
from typing import TYPE_CHECKING, ClassVar

import click

from chronovoyage.internal.type.dict import LogStyle

if TYPE_CHECKING:
    from collections.abc import Mapping


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
