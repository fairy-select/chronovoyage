from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Generator

import pytest
from click.testing import CliRunner
from support.database import SupportDbClass

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.config import (
    MigrateConfigGoSqlMissingError,
    MigrateConfigReturnSqlMissingError,
    MigrateConfigSqlMissingError,
    MigrateConfigVersionNameInvalidError,
)
from chronovoyage.internal.exception.domain import MigrateDomainInvalidTargetError
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod


class TestMigrateCommandMariadb:
    vendor = DatabaseVendorEnum.MARIADB
    # noinspection SqlResolve
    sql_select_all_from_user_order_by_id = "SELECT * FROM user ORDER BY id"

    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        self.support_db = SupportDbClass.get_class(self.vendor)
        yield
        self.support_db.truncate_test_db()

    def test_migrate_db_connect_fails(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            # when
            result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert result.stdout is not None, "explicitly log exceptions"
        assert result.exit_code == 1

    def test_ddl_only(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        os.chdir(resource_dir)
        # when
        CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert self.support_db.get_tables() == {"user", "category"}
        assert self.support_db.all_periods_have_come

    def test_period_name_invalid(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        os.chdir(resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigVersionNameInvalidError)

    def test_both_sqls_missing(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        os.chdir(resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigSqlMissingError)

    def test_go_sql_missing(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        os.chdir(resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigGoSqlMissingError)

    def test_return_sql_missing(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        os.chdir(resource_dir)
        # when
        result = CliRunner().invoke(chronovoyage, ["migrate"])
        # then
        assert isinstance(result.exception, MigrateConfigReturnSqlMissingError)

    def test_ddl_and_dml(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        os.chdir(resource_dir)
        # when
        runner.invoke(chronovoyage, ["migrate"])
        # then
        assert self.support_db.all_periods_have_come
        assert self.support_db.get_tables() == {"user"}
        # noinspection SqlResolve
        self.support_db.assert_rows_and_sql([(1, "Jane"), (2, "John")], self.sql_select_all_from_user_order_by_id)

    def test_migrate_from_zero_to_target(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"
        assert self.support_db.get_tables() == {"user"}
        # noinspection SqlResolve
        self.support_db.assert_rows_and_sql([(1, "Jane"), (2, "John")], self.sql_select_all_from_user_order_by_id)

    def test_migrate_from_halfway_to_latest(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["migrate"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235903"
        assert self.support_db.get_tables() == {"user"}
        # noinspection SqlResolve
        self.support_db.assert_rows_and_sql(
            [(1, "Jane"), (2, "John"), (3, "Allen"), (4, "Alicia")], self.sql_select_all_from_user_order_by_id
        )

    def test_migrate_from_halfway_to_target(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"
        assert self.support_db.get_tables() == {"user"}
        # noinspection SqlResolve
        self.support_db.assert_rows_and_sql([(1, "Jane"), (2, "John")], self.sql_select_all_from_user_order_by_id)

    def test_migrate_to_now(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"

    def test_migrate_to_past(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, MigrateDomainInvalidTargetError)
        assert period.period_name == "19991231235902"

    def test_migrate_to_unknown_target(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["migrate", "--target", "20060102150405"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, MigrateDomainInvalidTargetError)
        assert period.period_name == "19991231235902"

    def test_migrate_once_rolled_back_period(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
            # when
            result = runner.invoke(chronovoyage, ["migrate", "--target", "19991231235903"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert result.exception is None
        assert period.period_name == "19991231235903"
