import sys

import mariadb


class TestConnection:
    def test_connect_to_mariadb(self) -> None:
        try:
            conn = mariadb.connect(
                user="mariadb",
                password="password",
                host="127.0.0.1",
                port=3306,
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
