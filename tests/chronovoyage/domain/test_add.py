import os
import shutil

import pytest
from click.testing import CliRunner
from helper import TEST_TEMP_DIR
from typing_extensions import LiteralString

from chronovoyage.cli import chronovoyage
from chronovoyage.domain.add import AddDomain
from chronovoyage.internal.exception import DirectoryAlreadyExistsError
from chronovoyage.internal.exception.add_domain import AddDomainError, AddDomainInvalidDescriptionError
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum, MigratePeriodLanguageEnum
from chronovoyage.lib.datetime_time import DatetimeLib


class TestAddDomain:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()

    def test___init___non_existent_directory(self) -> None:
        # given
        target_dir = os.path.join(TEST_TEMP_DIR, "unknown")
        shutil.rmtree(target_dir, ignore_errors=True)
        # when
        with pytest.raises(AddDomainError):
            AddDomain(target_dir, logger=self.logger)

    @pytest.mark.parametrize("language", [pytest.param(lang) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor) for vendor in DatabaseVendorEnum])
    def test_execute(self, vendor: LiteralString, language: LiteralString) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            # when
            AddDomain(os.getcwd(), logger=self.logger).execute(
                MigratePeriodLanguageEnum(language),
                "sample_description",
                now=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1),
            )
            # then
            assert os.listdir(f"19991231235901_{language}_sample_description") == ["go.sql", "return.sql"]

    @pytest.mark.parametrize(
        "description",
        [
            pytest.param("full-time", id="cannot_use_hyphen"),
            pytest.param("hello world", id="cannot_use_space"),
        ],
    )
    @pytest.mark.parametrize("language", [pytest.param(lang) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor) for vendor in DatabaseVendorEnum])
    def test_execute__invalid_description_pattern(
        self, vendor: LiteralString, language: LiteralString, description: str
    ) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            # when/then
            with pytest.raises(AddDomainInvalidDescriptionError):
                AddDomain(os.getcwd(), logger=self.logger).execute(
                    MigratePeriodLanguageEnum(language),
                    description,
                    now=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1),
                )

    @pytest.mark.parametrize("language", [pytest.param(lang) for lang in MigratePeriodLanguageEnum])
    @pytest.mark.parametrize("vendor", [pytest.param(vendor) for vendor in DatabaseVendorEnum])
    def test_execute__cannot_create_same_directory(self, vendor: LiteralString, language: LiteralString) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", vendor])
            os.chdir("sample")
            AddDomain(os.getcwd(), logger=self.logger).execute(
                MigratePeriodLanguageEnum(language),
                "sample_description",
                now=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1),
            )
            # when/then
            with pytest.raises(DirectoryAlreadyExistsError):
                AddDomain(os.getcwd(), logger=self.logger).execute(
                    MigratePeriodLanguageEnum(language),
                    "sample_description",
                    now=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1),
                )
