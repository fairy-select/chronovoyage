import os
import subprocess
from unittest.mock import MagicMock

from click.testing import CliRunner
from pytest_mock import MockerFixture

from chronovoyage.cli import chronovoyage
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory


class TestCli:
    def test_with_no_command_and_no_options(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=True)
        assert result.stdout.startswith(b"Usage:"), "show help"

    def test_migrate_with_no_options(self, mocker: MockerFixture) -> None:
        # given
        m_config = MagicMock()
        m_create_config = mocker.patch.object(
            MigrateDomainConfigFactory, MigrateDomainConfigFactory.create_from_directory.__name__, return_value=m_config
        )
        m_instantiate = mocker.patch.object(MigrateDomain, MigrateDomain.__init__.__name__, return_value=None)
        m_execute = mocker.patch.object(MigrateDomain, MigrateDomain.execute.__name__)
        # when
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir("sample")
            runner.invoke(chronovoyage, ["migrate"])
            # then
            assert m_create_config.call_args[0] == (os.getcwd(),)
            assert m_instantiate.call_args[0] == (m_config,)
            assert m_execute.call_args[1] == {"target": None}

    def test_migrate_with_options(self, mocker: MockerFixture) -> None:
        # given
        m_config = MagicMock()
        m_create_config = mocker.patch.object(
            MigrateDomainConfigFactory, MigrateDomainConfigFactory.create_from_directory.__name__, return_value=m_config
        )
        m_instantiate = mocker.patch.object(MigrateDomain, MigrateDomain.__init__.__name__, return_value=None)
        m_execute = mocker.patch.object(MigrateDomain, MigrateDomain.execute.__name__)
        # when
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir("sample")
            runner.invoke(chronovoyage, ["migrate", "--target", "20060102150405"])
            # then
            assert m_create_config.call_args[0] == (os.getcwd(),)
            assert m_instantiate.call_args[0] == (m_config,)
            assert m_execute.call_args[1] == {"target": "20060102150405"}
