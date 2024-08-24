import subprocess


class TestCli:
    def test_with_no_option(self) -> None:
        result = subprocess.run(["chronovoyage"], capture_output=True, check=False)
        result.check_returncode()
        assert result.stdout.rstrip() == b"Hello world!"
