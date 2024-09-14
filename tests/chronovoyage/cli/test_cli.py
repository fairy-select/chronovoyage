import os
import subprocess
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from chronovoyage.cli import chronovoyage
from chronovoyage.domain.add import AddDomain
from chronovoyage.domain.init import InitDomain
from chronovoyage.domain.migrate import MigrateDomain
from chronovoyage.internal.config import MigrateDomainConfigFactory
from chronovoyage.internal.type.enum import DatabaseVendorEnum, MigratePeriodLanguageEnum
from chronovoyage.lib.datetime_time import DatetimeLib


class TestCli:
    def test_with_no_command_and_no_options(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=True)
        assert result.stdout.startswith(b"Usage:"), "show help"

    @pytest.mark.parametrize(
        "command",
        [
            pytest.param("init"),
        ],
    )
    def test_with_command_and_no_options(self, command: str) -> None:
        result = subprocess.run(["chronovoyage", command], capture_output=True, check=False)
        assert result.stderr.startswith(b"Usage:"), "show help"

    @pytest.mark.parametrize("vendor", [pytest.param(vendor.value) for vendor in DatabaseVendorEnum])
    def test_init(self, mocker: MockerFixture, vendor: str) -> None:
        # given
        m_instantiate = mocker.patch.object(InitDomain, InitDomain.__init__.__name__, return_value=None)
        m_execute = mocker.patch.object(InitDomain, InitDomain.execute.__name__)
        # when
        CliRunner().invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
        # then
        assert m_instantiate.call_args.args == (os.getcwd(),)
        assert m_execute.call_args.args == ("sample", DatabaseVendorEnum("mariadb"))

    def test_init__default_vendor_is_mariadb(self, mocker: MockerFixture) -> None:
        # given
        m_instantiate = mocker.patch.object(InitDomain, InitDomain.__init__.__name__, return_value=None)
        m_execute = mocker.patch.object(InitDomain, InitDomain.execute.__name__)
        # when
        CliRunner().invoke(chronovoyage, ["init", "sample"])
        # then
        assert m_instantiate.call_args.args == (os.getcwd(),)
        assert m_execute.call_args.args == ("sample", DatabaseVendorEnum("mariadb"))

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

    @pytest.mark.parametrize("language", [pytest.param(lang.value) for lang in MigratePeriodLanguageEnum])
    def test_add(self, mocker: MockerFixture, language: str) -> None:
        m_now = DatetimeLib.datetime(1999, 12, 31, 23, 59, 1)
        _ = mocker.patch.object(DatetimeLib, DatetimeLib.now.__name__, return_value=m_now)
        _ = mocker.patch.object(MigrateDomainConfigFactory, MigrateDomainConfigFactory.create_from_directory.__name__)
        _ = mocker.patch.object(AddDomain, AddDomain.__init__.__name__, return_value=None)
        m_execute = mocker.patch.object(AddDomain, AddDomain.execute.__name__)
        # when
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(chronovoyage, ["add", language, "sample_description"])
            # then
            assert m_execute.call_args.args == (MigratePeriodLanguageEnum(language), "sample_description")
            assert m_execute.call_args.kwargs == {"now": m_now}
