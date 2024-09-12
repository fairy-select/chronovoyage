from __future__ import annotations

import pytest
from helper.database.mariadb import get_default_mariadb_connection, mariadb_get_tables

from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.logger import get_default_logger


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()
        self.config_factory = MigrateDomainConfigFactory()

    # noinspection PyMethodMayBeStatic
    def _get_tables(self) -> set[str]:
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            return mariadb_get_tables(cursor)

    @property
    def _all_periods_have_come(self) -> bool:
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SELECT has_come FROM chronovoyage_periods")
            return {has_come for (has_come,) in cursor.fetchall()} == {True}

    @property
    def _current_period(self) -> str | None:
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            cursor.execute("SELECT period_name FROM chronovoyage_periods WHERE has_come IS TRUE ORDER BY id DESC")
            row = cursor.fetchone()
            if row is None:
                return None
            (period_name,) = row
            return period_name

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
        want_users = [(1, 'Jane'), (2, 'John')]
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT * FROM user ORDER BY id")
            if cursor.rowcount != len(want_users):
                pytest.fail(f"件数が異なる (want: {len(want_users)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_users[i], f"row {i}"

    @pytest.mark.skip
    def test_partially_migrate(self, mariadb_migrate_domain_config) -> None:
        # when
        MigrateDomain(mariadb_migrate_domain_config, logger=self.logger).execute()
        # then
        assert self._current_period == "19991231235902"
        want_users = [(1, 'Jane'), (2, 'John')]
        with get_default_mariadb_connection() as wrapper:
            cursor = wrapper.cursor()
            # noinspection SqlResolve
            cursor.execute("SELECT * FROM user ORDER BY id")
            if cursor.rowcount != len(want_users):
                pytest.fail(f"件数が異なる (want: {len(want_users)}), got: {cursor.rowcount}")
            for i, got_user in enumerate(cursor):
                assert got_user == want_users[i], f"row {i}"
