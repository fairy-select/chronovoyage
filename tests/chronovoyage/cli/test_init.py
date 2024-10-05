import json
import os.path
import subprocess
from typing import Mapping

import pytest
from click.testing import CliRunner

from chronovoyage.cli import chronovoyage
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


class TestInitCommand:
    def test_with_command_and_no_options(self) -> None:
        result = subprocess.run(["chronovoyage", "init"], capture_output=True, check=False)
        assert result.stderr.startswith(b"Usage:"), "show help"

    def test_default_vendor_is_mariadb(self) -> None:
        # given
        runner = CliRunner()
        with runner.isolated_filesystem():
            # when
            runner.invoke(chronovoyage, ["init", "sample"])
            # then
            with open(os.path.join(os.getcwd(), "sample", "config.json")) as f:
                config = f.read()
                assert json.loads(config)["vendor"] == "mariadb"

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
