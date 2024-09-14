import os
import shutil

import pytest
from click.testing import CliRunner
from helper import TEST_TEMP_DIR

from chronovoyage.cli import chronovoyage
from chronovoyage.domain.add import AddDomain
from chronovoyage.internal.exception.add_domain import AddDomainError
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import MigratePeriodLanguageEnum
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

    @pytest.mark.parametrize("language", [pytest.param(lang.value) for lang in MigratePeriodLanguageEnum])
    def test_execute(self, language: str) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            runner.invoke(chronovoyage, ["init", "sample", "--vendor", "mariadb"])
            os.chdir("sample")
            # when
            AddDomain(os.getcwd(), logger=self.logger).execute(
                MigratePeriodLanguageEnum(language),
                "sample_description",
                now=DatetimeLib.datetime(1999, 12, 31, 23, 59, 1),
            )
            # then
            assert os.listdir(f"19991231235901_{language}_sample_description") == ["go.sql", "return.sql"]
