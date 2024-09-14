# SPDX-FileCopyrightText: 2024-present Noritaka IZUMI <noritaka.izumi@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os.path

import click

from chronovoyage.__about__ import __version__
from chronovoyage.domain.init import InitDomain
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum

logger = get_default_logger()
database_vendors = [getattr(e, "value") for e in DatabaseVendorEnum]


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="chronovoyage")
def chronovoyage():
    pass


@chronovoyage.command()
@click.argument("dirname", type=click.STRING)
@click.option(
    "--vendor",
    "-v",
    type=click.Choice(database_vendors, case_sensitive=False),
    default=DatabaseVendorEnum.MARIADB,
    help="Database vendor.",
)
def init(dirname: str, vendor: str):
    """Create chronovoyage config directory and initialize."""
    InitDomain(os.getcwd(), logger=logger).execute(dirname, DatabaseVendorEnum(vendor))


@chronovoyage.command()
@click.option("--target", "-t", help="Move to a specific period. (Example: 20060102150405)")
@click.argument("path", type=click.Path(exists=True))
def migrate(path: str, target: str | None):
    MigrateDomain(MigrateDomainConfigFactory.create_from_directory(os.path.realpath(path)), logger=logger).execute(
        target=target
    )
