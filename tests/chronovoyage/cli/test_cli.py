import subprocess

import pytest


class TestCli:
    def test_with_no_option(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=False)
        result.check_returncode()
        assert result.stdout.startswith(b"Usage:"), "show help"

    @pytest.mark.skip(reason="no option should show help")  # TODO: implement
    def test_migrate(self) -> None:
        _ = subprocess.run(["chronovoyage", "migrate"], capture_output=True, check=True)
