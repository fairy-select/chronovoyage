import subprocess

import pytest


class TestCli:
    def test_with_no_command_and_no_options(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=True)
        assert result.stdout.startswith(b"Usage:"), "show help"

    @pytest.mark.parametrize(
        "command",
        [
            pytest.param("init"),
            pytest.param("migrate"),
        ],
    )
    def test_with_command_and_no_options(self, command: str) -> None:
        result = subprocess.run(["chronovoyage", command], capture_output=True, check=False)
        assert result.stderr.startswith(b"Usage:"), "show help"
