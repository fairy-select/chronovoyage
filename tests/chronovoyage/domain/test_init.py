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

    def test_execute(self) -> None:
        # when
        dirname = "sample"
        InitDomain(TEST_TEMP_DIR, logger=self.logger).execute(dirname)
        # then
        assert os.listdir(os.path.join(TEST_TEMP_DIR, dirname)) == ["config.json"]
        with open(os.path.join(TEST_TEMP_DIR, dirname, "config.json"), "r") as f:
            config = f.read()
        assert config == """
{
  "$schema": "https://raw.githubusercontent.com/noritakaIzumi/chronovoyage/main/schema/config.schema.json",
  "vendor": "mariadb",
  "connection_info": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "mariadb",
    "password": "password",
    "database": "test"
  }
}
""".strip() + "\n"
