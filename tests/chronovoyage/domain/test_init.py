import os.path
import shutil

import pytest
from helper import TEST_TEMP_DIR

from chronovoyage.domain.init import InitDomain
from chronovoyage.internal.exception.init import InitDomainError
from chronovoyage.internal.logger import get_default_logger


class TestInitDomain:
    @pytest.fixture(autouse=True)
    def _(self) -> None:
        self.logger = get_default_logger()

    def test___init___non_existent_directory(self) -> None:
        # given
        target_dir = os.path.join(TEST_TEMP_DIR, "unknown")
        shutil.rmtree(target_dir, ignore_errors=True)
        # when
        with pytest.raises(InitDomainError):
            InitDomain(target_dir, logger=self.logger)
