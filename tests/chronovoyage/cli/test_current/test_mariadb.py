from __future__ import annotations

import os
import shutil
from typing import Any, Generator

import pytest
from click.testing import CliRunner
from support.database.mariadb_ import SupportMariadb

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.current import CurrentDbCurrentPeriodNotInMigrateConfigError


class TestCurrentCommandMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        yield
        SupportMariadb.truncate_mariadb_test_db()

    def test_current_is_latest(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert "Current period: 19991231235902 ddl sample02" in result.stdout.splitlines()

    def test_current_is_halfway(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert "Current period: 19991231235901 ddl sample01" in result.stdout.splitlines()

    def test_current_is_not_in_config(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            shutil.copytree(mariadb_resource_dir, "migrations")
            os.chdir("migrations")
            runner.invoke(chronovoyage, ["migrate"])
            for f in os.listdir(mariadb_resource_dir):
                if os.path.isdir(f):
                    shutil.rmtree(f)
            # when
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert isinstance(result.exception, CurrentDbCurrentPeriodNotInMigrateConfigError)
