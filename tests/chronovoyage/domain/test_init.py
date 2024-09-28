import os.path
import shutil
from typing import Mapping
from typing_extensions import LiteralString

import pytest

from chronovoyage.domain.init import InitDomain
from chronovoyage.internal.exception.init import InitDomainError
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum
from helper import TEST_TEMP_DIR


def _want_config(vendor: DatabaseVendorEnum) -> str:
    vendor_to_config: Mapping[DatabaseVendorEnum, str] = {
        DatabaseVendorEnum.MARIADB: """
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
""".strip()
        + "\n",
    }
    return vendor_to_config[vendor]


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

    @pytest.mark.parametrize(
        ("vendor", "want_config"),
        [pytest.param(vendor, _want_config(DatabaseVendorEnum(vendor)), id=vendor) for vendor in DatabaseVendorEnum],
    )
    def test_execute(self, vendor: LiteralString, want_config: str) -> None:
        # given
        dirname = "sample"
        # when
        InitDomain(TEST_TEMP_DIR, logger=self.logger).execute(dirname, DatabaseVendorEnum(vendor))
        # then
        assert os.listdir(os.path.join(TEST_TEMP_DIR, dirname)) == ["config.json"]
        with open(os.path.join(TEST_TEMP_DIR, dirname, "config.json")) as f:
            config = f.read()
        assert config == want_config
