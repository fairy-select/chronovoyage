# SPDX-FileCopyrightText: 2024-present Noritaka IZUMI <noritaka.izumi@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os.path

import click
from click import Group

from chronovoyage.__about__ import __version__
from chronovoyage.domain.add import AddDomain
from chronovoyage.domain.current import CurrentDomain
from chronovoyage.domain.init import InitDomain
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.domain.rollback import RollbackDomain
from chronovoyage.internal.config import MigrateConfigFactory
from chronovoyage.internal.feature.flags import FeatureFlagEnabledChecker
from chronovoyage.internal.logger.logger import AppLoggerFactory, get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum, MigratePeriodLanguageEnum
from chronovoyage.lib.datetime_time import DatetimeLib

database_vendors = [e.value for e in DatabaseVendorEnum]
migrate_period_languages = [e.value for e in MigratePeriodLanguageEnum]

chronovoyage: Group


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)  # type: ignore[no-redef]
@click.version_option(version=__version__, prog_name="chronovoyage")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Enable verbose log.")
def chronovoyage(*, verbose: bool):
    AppLoggerFactory.set_verbose(verbose=verbose)


@chronovoyage.command()
@click.argument("dirname", type=click.STRING)
@click.option(
    "--vendor",
    type=click.Choice(database_vendors, case_sensitive=False),
    default=DatabaseVendorEnum.MARIADB.value,
    help="Database vendor.",
)
def init(dirname: str, vendor: str):
    """Create chronovoyage config directory and initialize."""
    InitDomain(os.getcwd(), logger=get_default_logger()).execute(dirname, DatabaseVendorEnum(vendor))


@chronovoyage.command()
@click.argument("language", type=click.Choice(migrate_period_languages, case_sensitive=False))
@click.argument("description", type=click.STRING)
def add(language: str, description: str):
    """Add migration period to your directory."""
    AddDomain(os.getcwd(), logger=get_default_logger()).execute(
        MigratePeriodLanguageEnum(language), description, now=DatetimeLib.now()
    )


@chronovoyage.command()
def current():
    """Get current period."""
    period = CurrentDomain(
        MigrateConfigFactory.create_from_directory(os.getcwd()), logger=get_default_logger()
    ).execute()
    click.echo(f"Current period: {period.period_name} {period.language} {period.description}")
    return period


@chronovoyage.command()
@click.option("--target", "-t", help="Move to a specific period. (Example: 20060102150405)")
def migrate(target: str | None):
    """Migrate database. Use \"rollback\" if you move to a previous version."""
    MigrateDomain(MigrateConfigFactory.create_from_directory(os.getcwd()), logger=get_default_logger()).execute(
        target=target
    )


@chronovoyage.command()
@click.option("--target", "-t", help="Move to a specific period. (Example: 20060102150405)")
def rollback(target: str | None):
    """Rollback database."""
    if target is None:
        FeatureFlagEnabledChecker.rollback_without_options()
    RollbackDomain(MigrateConfigFactory.create_from_directory(os.getcwd()), logger=get_default_logger()).execute(
        target=target
    )
