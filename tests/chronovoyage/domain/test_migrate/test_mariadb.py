from __future__ import annotations

from typing import Any

import mariadb
import pytest
from helper.database.mariadb_ import get_default_mariadb_connection, mariadb_get_tables

from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.exception.migrate import MigrateInvalidTargetError
from chronovoyage.internal.logger import get_default_logger


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()
        self.config_factory = MigrateDomainConfigFactory()

    # noinspection PyMethodMayBeStatic
    def _get_tables(self) -> set[str]:
        with get_default_mariadb_connection() as wrapper:
            with wrapper._begin() as conn:
                cursor = conn.cursor()
                return mariadb_get_tables(cursor)

    @property
    def _all_periods_have_come(self) -> bool:
        with get_default_mariadb_connection() as wrapper:
            with wrapper._begin() as conn:
                cursor = conn.cursor()
                # noinspection SqlResolve
                cursor.execute("SELECT has_come FROM chronovoyage_periods")
                return {has_come for (has_come,) in cursor.fetchall()} == {True}

    # noinspection PyMethodMayBeStatic
    def assert_rows_and_sql(self, want_rows: list[tuple[Any, ...]], sql: str) -> None:
        with get_default_mariadb_connection() as wrapper:
            with wrapper._begin() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                if cursor.rowcount != len(want_rows):
                    pytest.fail(f"件数が異なる (want: {len(want_rows)}), got: {cursor.rowcount}")
                for i, got_user in enumerate(cursor):
                    assert got_user == want_rows[i], f"row {i}"

    def test_ddl_only(self, mariadb_migrate_domain_config) -> None:
        # when
        MigrateDomain(mariadb_migrate_domain_config, logger=self.logger).execute()
        # then
        assert self._get_tables() == {"user", "category"}
        assert self._all_periods_have_come

    def test_period_name_invalid(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigVersionNameInvalidError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_both_sqls_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_go_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigGoSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_return_sql_missing(self, mariadb_resource_dir) -> None:
        with pytest.raises(MigrateConfigReturnSqlMissingError):
            _ = self.config_factory.create_from_directory(mariadb_resource_dir)

    def test_ddl_and_dml(self, mariadb_migrate_domain_config) -> None:
        # when
        MigrateDomain(mariadb_migrate_domain_config, logger=self.logger).execute()
        # then
        assert self._all_periods_have_come
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

    def test_migrate_from_zero_to_target(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        # when
        migrate_domain.execute(target="19991231235902")
        # then
        assert migrate_domain.usecase.current() == "19991231235902"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

    def test_migrate_from_halfway_to_latest(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        migrate_domain.execute(target="19991231235902")
        # when
        migrate_domain.execute()
        # then
        assert migrate_domain.usecase.current() == "19991231235903"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql(
            [(1, "Jane"), (2, "John"), (3, "Allen"), (4, "Alicia")], "SELECT * FROM user ORDER BY id"
        )

    def test_migrate_from_halfway_to_target(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        migrate_domain.execute(target="19991231235901")
        # when
        migrate_domain.execute(target="19991231235902")
        # then
        assert migrate_domain.usecase.current() == "19991231235902"
        assert self._get_tables() == {"user"}
        # noinspection SqlResolve
        self.assert_rows_and_sql([(1, "Jane"), (2, "John")], "SELECT * FROM user ORDER BY id")

    def test_migrate_to_now(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        migrate_domain.execute(target="19991231235902")
        # when
        migrate_domain.execute(target="19991231235902")
        # then
        assert migrate_domain.usecase.current() == "19991231235902"

    def test_migrate_to_past(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        migrate_domain.execute(target="19991231235902")
        # when
        with pytest.raises(MigrateInvalidTargetError):
            migrate_domain.execute(target="19991231235901")
        # then
        assert migrate_domain.usecase.current() == "19991231235902"

    def test_migrate_to_unknown_target(self, mariadb_migrate_domain_config) -> None:
        # given
        migrate_domain = MigrateDomain(mariadb_migrate_domain_config, logger=self.logger)
        # when
        with pytest.raises(MigrateInvalidTargetError):
            migrate_domain.execute(target="20060102150405")
        # then
        with pytest.raises(mariadb.ProgrammingError):
            migrate_domain.usecase.current()
        assert self._get_tables() == set()
