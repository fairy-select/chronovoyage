import os

from dotenv import dotenv_values

from chronovoyage.internal.type.database import ConnectionInfo

TESTS_DIR = os.path.realpath(f"{os.path.dirname(__file__)}/..")
RESOURCE_DIR = f"{TESTS_DIR}/resource"
DEFAULT_TEST_ENV = dotenv_values(f"{TESTS_DIR}/test.env")


def default_mariadb_connection_info() -> ConnectionInfo:
    return ConnectionInfo(
        host="127.0.0.1",
        port=3307,
        user=DEFAULT_TEST_ENV["MARIADB_USER"],
        password=DEFAULT_TEST_ENV["MARIADB_PASSWORD"],
        database=DEFAULT_TEST_ENV["MARIADB_DATABASE"],
    )
