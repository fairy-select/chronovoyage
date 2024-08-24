import sys
from typing import Literal

from helper import DEFAULT_TEST_ENV

DatabaseVendor = Literal["mariadb"]


class DatabaseHelper:
    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendor):
        if vendor == "mariadb":
            import mariadb
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

            return conn

        return None
