from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Generator

import pytest
from click.testing import CliRunner
from helper.database.mariadb_ import get_default_mariadb_connection, mariadb_get_tables, truncate_mariadb_test_db

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.exception.migrate import MigrateInvalidTargetError

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod


class TestMigrateCommandMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        yield
        truncate_mariadb_test_db()

    # noinspection PyMethodMayBeStatic
    def _get_tables(self) -> set[str]:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            return mariadb_get_tables(cursor)

    @property
    def _all_periods_have_come(self) -> bool:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT has_come FROM chronovoyage_periods")
            return {has_come for (has_come,) in cursor.fetchall()} == {True}

    # noinspection PyMethodMayBeStatic
    def assert_rows_and_sql(self, want_rows: list[tuple[Any, ...]], sql: str) -> None:
        with get_default_mariadb_connection() as wrapper, wrapper.begin() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if cursor.rowcount != len(want_rows):
                pytest.fail(f"件数が異なる (want: {len(want_rows)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_rows[i], f"row {i}"

    def test_ddl_only(self, mariadb_resource_dir) -> None:
        # given
        os.chdir(mariadb_resource_dir)
        # when
        CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert self._get_tables() == {"user", "category"}
        assert self._all_periods_have_come

    def test_period_name_invalid(self, mariadb_resource_dir) -> None:
        # given
        os.chdir(mariadb_resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigVersionNameInvalidError)

    def test_both_sqls_missing(self, mariadb_resource_dir) -> None:
        # given
        os.chdir(mariadb_resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigSqlMissingError)

    def test_go_sql_missing(self, mariadb_resource_dir) -> None:
        # given
        os.chdir(mariadb_resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigGoSqlMissingError)

    def test_return_sql_missing(self, mariadb_resource_dir) -> None:
        # given
        os.chdir(mariadb_resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigReturnSqlMissingError)

    def test_ddl_and_dml(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        os.chdir(mariadb_resource_dir)
        # when
        runner.invoke(chronovoyage, ["migrate"])
        # then
        assert self._all_periods_have_come
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

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
