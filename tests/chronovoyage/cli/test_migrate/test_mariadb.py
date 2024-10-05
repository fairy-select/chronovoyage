from __future__ import annotations

import os
from typing import Any, Generator

import pytest
from click.testing import CliRunner

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from helper.database.mariadb_ import get_default_mariadb_connection, mariadb_get_tables, truncate_mariadb_test_db


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
