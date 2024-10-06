import os
import shutil
from typing import TYPE_CHECKING, Any, Generator

import pytest
from click.testing import CliRunner
from support.database import SupportDbClass

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.feature import FeatureNotSupportedError
from chronovoyage.internal.exception.migrate import (
    RollbackFutureTargetError,
    RollbackInvalidTargetError,
    RollbackMigratedPeriodNotInMigrateConfigError,
    RollbackSystemTableNotExistError,
)
from chronovoyage.internal.type.enum import DatabaseVendorEnum

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod


class TestRollbackCommandMariadb:
    vendor = DatabaseVendorEnum.MARIADB

    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        self.support_db = SupportDbClass.get_class(self.vendor)
        yield
        self.support_db.truncate_test_db()

    def test_rollback_with_no_options(self, resource_dir_factory) -> None:
        """オプションなしで 1 時代のみ巻き戻す機能。現在未実装。"""
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["rollback"])
        # then
        # TODO: implement and fix assertion
        assert isinstance(result.exception, FeatureNotSupportedError)

    def test_rollback_from_latest_to_halfway(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert result.exit_code == 0
        assert period.period_name == "19991231235901"

    def test_rollback_to_now(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["rollback", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"

    def test_rollback_from_halfway_to_target(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235901"
        assert self.support_db.get_tables() == {"user"}
        # noinspection SqlResolve
        self.support_db.assert_rows_and_sql([], "SELECT * FROM user ORDER BY id")

    def test_rollback_to_future(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, RollbackFutureTargetError)
        assert period.period_name == "19991231235901"

    def test_rollback_from_nothing(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
        # then
        assert isinstance(result.exception, RollbackSystemTableNotExistError)

    def test_rollback_to_unknown_target(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991130123456"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, RollbackInvalidTargetError)
        assert period.period_name == "19991231235902"

    def test_rollback_config_is_missing(self, resource_dir_factory) -> None:
        # given
        resource_dir = resource_dir_factory.get_directory(self.vendor)
        runner = CliRunner()
        with runner.isolated_filesystem():
            shutil.copytree(resource_dir, "migrations")
            os.chdir("migrations")
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            for f in os.listdir(resource_dir):
                if os.path.isdir(f) and f.startswith("19991231235902"):
                    shutil.rmtree(f)
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
        # then
        assert isinstance(result.exception, RollbackMigratedPeriodNotInMigrateConfigError)
