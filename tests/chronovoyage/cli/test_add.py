import os

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from chronovoyage.cli import chronovoyage
from chronovoyage.internal.exception import DirectoryAlreadyExistsError
from chronovoyage.internal.exception.domain import AddDomainInvalidDescriptionError
from chronovoyage.internal.type.enum import DatabaseVendorEnum, MigratePeriodLanguageEnum
from chronovoyage.lib.datetime_time import DatetimeLib


class TestAddCommand:
    @pytest.mark.parametrize("language", [pytest.param(lang.value) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor.value) for vendor in DatabaseVendorEnum])
    def test_execute(self, mocker: MockerFixture, vendor: str, language: str) -> None:
        # given
        mocker.patch.object(
            DatetimeLib, DatetimeLib.now.__name__, return_value=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1)
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            # when
            runner.invoke(chronovoyage, ["add", language, "sample_description"])
            # then
            assert os.listdir(f"19991231235901_{language}_sample_description") == ["go.sql", "return.sql"]

    @pytest.mark.parametrize(
        "description",
        [
            pytest.param("full-time", id="cannot_use_hyphen"),
            pytest.param("hello world", id="cannot_use_space"),
        ],
    )
    @pytest.mark.parametrize("language", [pytest.param(lang.value) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor.value) for vendor in DatabaseVendorEnum])
    def test_execute__invalid_description_pattern(
        self, mocker: MockerFixture, vendor: str, language: str, description: str
    ) -> None:
        # given
        mocker.patch.object(
            DatetimeLib, DatetimeLib.now.__name__, return_value=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1)
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            # when
            result = runner.invoke(chronovoyage, ["add", language, description])
        # then
        assert isinstance(result.exception, AddDomainInvalidDescriptionError)

    @pytest.mark.parametrize("language", [pytest.param(lang.value) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor.value) for vendor in DatabaseVendorEnum])
    def test_execute__cannot_create_same_directory(self, mocker: MockerFixture, vendor: str, language: str) -> None:
        # given
        mocker.patch.object(
            DatetimeLib, DatetimeLib.now.__name__, return_value=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1)
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            runner.invoke(chronovoyage, ["add", language, "sample_description"])
            # when
            result = runner.invoke(chronovoyage, ["add", language, "sample_description"])
        # then
        assert isinstance(result.exception, DirectoryAlreadyExistsError)
