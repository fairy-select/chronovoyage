import os
import shutil

import pytest
from click.testing import CliRunner

from chronovoyage.domain.add import AddDomain
from chronovoyage.internal.exception.add_domain import AddDomainError
from chronovoyage.internal.logger import get_default_logger


class TestAddDomain:
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
            with pytest.raises(AddDomainError):
                AddDomain(target_dir, logger=self.logger)
