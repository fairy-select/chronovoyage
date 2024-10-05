import os
from typing import TYPE_CHECKING, Any, Generator

import pytest
from click.testing import CliRunner

from chronovoyage.internal.exception.migrate import RollbackFutureTargetError, RollbackSystemTableNotExistError, \
    RollbackInvalidTargetError
from support.database.mariadb_ import SupportMariadb

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception.feature import FeatureNotSupportedError

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod


class TestRollbackCommandMariadb:
    @pytest.fixture(autouse=True)
    def _(self) -> Generator[Any, Any, None]:
        yield
        SupportMariadb.truncate_mariadb_test_db()

    def test_rollback_with_no_options(self, mariadb_resource_dir) -> None:
        """オプションなしで 1 時代のみ巻き戻す機能。現在未実装。"""
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["rollback"])
        # then
        # TODO: implement and fix assertion
        assert isinstance(result.exception, FeatureNotSupportedError)

    def test_rollback_from_latest_to_halfway(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert result.exit_code == 0
        assert period.period_name == "19991231235901"

    def test_rollback_to_now(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["rollback", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235902"

    def test_rollback_from_halfway_to_target(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert period.period_name == "19991231235901"
        assert SupportMariadb.get_tables() == {"user"}
        # noinspection SqlResolve
        SupportMariadb.assert_rows_and_sql([], "SELECT * FROM user ORDER BY id")

    def test_rollback_to_future(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235901"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235902"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, RollbackFutureTargetError)
        assert period.period_name == "19991231235901"

    def test_rollback_from_nothing(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991231235901"])
        # then
        assert isinstance(result.exception, RollbackSystemTableNotExistError)

    def test_rollback_to_unknown_target(self, mariadb_resource_dir) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.chdir(mariadb_resource_dir)
            runner.invoke(chronovoyage, ["migrate", "--target", "19991231235902"])
            # when
            result = runner.invoke(chronovoyage, ["rollback", "--target", "19991130123456"])
            period: MigratePeriod = runner.invoke(chronovoyage, ["current"], standalone_mode=False).return_value
        # then
        assert isinstance(result.exception, RollbackInvalidTargetError)
        assert period.period_name == "19991231235902"
