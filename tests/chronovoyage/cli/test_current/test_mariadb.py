from __future__ import annotations

import os
import shutil
from typing import Any, Generator

import pytest
from click.testing import CliRunner
from support.database import SupportDbClass

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.domain import CurrentDomainDbCurrentPeriodNotInMigrateConfigError
from chronovoyage.internal.type.enum import DatabaseVendorEnum


class TestCurrentCommandMariadb:
    vendor = DatabaseVendorEnum.MARIADB

    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        self.support_db = SupportDbClass.get_class(self.vendor)
        yield
        self.support_db.truncate_test_db()

    def test_current_without_migration_periods(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert "No migration periods." in result.stdout.splitlines()

    def test_current_is_latest(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert "Current period: 19991231235902 ddl sample02" in result.stdout.splitlines()

    def test_current_is_halfway(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert "Current period: 19991231235901 ddl sample01" in result.stdout.splitlines()

    def test_current_is_not_in_config(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            shutil.copytree(resource_dir, "migrations")
            os.chdir("migrations")
            runner.invoke(chronovoyage, ["migrate"])
            for f in os.listdir(resource_dir):
                if os.path.isdir(f):
                    shutil.rmtree(f)
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert isinstance(result.exception, CurrentDomainDbCurrentPeriodNotInMigrateConfigError)
