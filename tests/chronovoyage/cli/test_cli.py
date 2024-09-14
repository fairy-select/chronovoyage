import subprocess


class TestCli:
    def test_with_no_command_and_no_option(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=True)
        assert result.stdout.startswith(b"Usage:"), "show help"

    def test_migrate_with_no_options(self) -> None:
        result = subprocess.run(["chronovoyage", "migrate"], capture_output=True, check=False)
        assert result.stderr.startswith(b"Usage:"), "show help"
