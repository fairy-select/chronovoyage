import os
import shutil

import pytest
from click.testing import CliRunner

from chronovoyage.domain.init import InitDomain
from chronovoyage.internal.exception.domain import InitDomainError
from chronovoyage.internal.logger.logger import get_default_logger


class TestInitDomain:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()

    def test___init___non_existent_directory(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            cwd = os.getcwd()
            target_dir = os.path.join(cwd, "unknown")
            shutil.rmtree(target_dir, ignore_errors=True)
            # when/then
            with pytest.raises(InitDomainError):
                InitDomain(target_dir, logger=self.logger)
