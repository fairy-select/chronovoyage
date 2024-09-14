import os
import shutil

import pytest

from chronovoyage.domain.add import AddDomain
from chronovoyage.internal.exception.add_domain import AddDomainError
from chronovoyage.internal.logger import get_default_logger
from helper import TEST_TEMP_DIR


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
