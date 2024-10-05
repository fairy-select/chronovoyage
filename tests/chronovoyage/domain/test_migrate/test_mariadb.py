from __future__ import annotations

from typing import Any, Generator

import mariadb
import pytest
from helper.database.mariadb_ import get_default_mariadb_connection, mariadb_get_tables, truncate_mariadb_test_db

from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.exception.migrate import MigrateInvalidTargetError
from chronovoyage.internal.logger import get_default_logger


class TestMigrateDomainMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        self.logger = get_default_logger()
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
