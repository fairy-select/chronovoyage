import os.path
import shutil
from typing import Mapping

import pytest
from click.testing import CliRunner

from chronovoyage.cli import chronovoyage
from chronovoyage.domain.init import InitDomain
from chronovoyage.internal.exception.init import InitDomainError
from chronovoyage.internal.logger import get_default_logger
from chronovoyage.internal.type.enum import DatabaseVendorEnum


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
        runner = CliRunner()
        with runner.isolated_filesystem():
            # given
            cwd = os.getcwd()
            target_dir = os.path.join(cwd, "unknown")
            shutil.rmtree(target_dir, ignore_errors=True)
            # when/then
            with pytest.raises(InitDomainError):
                InitDomain(target_dir, logger=self.logger)

    @pytest.mark.parametrize(
        ("vendor", "want_config"),
        [pytest.param(vendor, _want_config(vendor), id=vendor.value) for vendor in DatabaseVendorEnum],
    )
    def test_execute(self, vendor: DatabaseVendorEnum, want_config: str) -> None:
        # given
        dirname = "sample"
        # when
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(chronovoyage, ["init", dirname, "--vendor", vendor.value])
            # then
            cwd = os.getcwd()
            assert os.listdir(os.path.join(cwd, dirname)) == ["config.json"]
            with open(os.path.join(cwd, dirname, "config.json")) as f:
                config = f.read()
            assert config == want_config
