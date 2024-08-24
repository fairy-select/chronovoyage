import sys

import mariadb

from helper import DEFAULT_TEST_ENV


class TestConnection:
    def test_connect_to_mariadb(self) -> None:
        try:
            conn = mariadb.connect(
                user=DEFAULT_TEST_ENV["MARIADB_USER"],
                password=DEFAULT_TEST_ENV["MARIADB_PASSWORD"],
                host="127.0.0.1",
                port=3307,
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
