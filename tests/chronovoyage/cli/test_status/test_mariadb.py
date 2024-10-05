from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, Any, Generator

import pytest
from click.testing import CliRunner
from helper.database.mariadb_ import get_default_mariadb_connection, mariadb_get_tables, truncate_mariadb_test_db

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.current import CurrentDbCurrentPeriodNotInMigrateConfigError
from chronovoyage.internal.exception.migrate import MigrateInvalidTargetError

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod


class TestCurrentCommandMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        yield
        truncate_mariadb_test_db()

    # noinspection PyMethodMayBeStatic
    def _get_tables(self) -> set[str]:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            return mariadb_get_tables(cursor)

    # noinspection PyMethodMayBeStatic
    def assert_rows_and_sql(self, want_rows: list[tuple[Any, ...]], sql: str) -> None:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if cursor.rowcount != len(want_rows):
                pytest.fail(f"件数が異なる (want: {len(want_rows)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_rows[i], f"row {i}"

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
            # when
            for f in os.listdir(mariadb_resource_dir):
                if os.path.isdir(f):
                    shutil.rmtree(f)
            result = runner.invoke(chronovoyage, ["current"])
        # then
        assert isinstance(result.exception, CurrentDbCurrentPeriodNotInMigrateConfigError)

    def test_migrate_from_zero_to_target(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

    def test_migrate_from_halfway_to_latest(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["migrate"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235903"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql(
            [(1, "Jane"), (2, "John"), (3, "Allen"), (4, "Alicia")], "SELECT * FROM user ORDER BY id"
        )

    def test_migrate_from_halfway_to_target(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

    def test_migrate_to_now(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"

    def test_migrate_to_past(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, MigrateInvalidTargetError)
        assert period.period_name == "19991231235902"

    def test_migrate_to_unknown_target(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["migrate", "--target", "20060102150405"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, MigrateInvalidTargetError)
        assert period.period_name == "19991231235902"
