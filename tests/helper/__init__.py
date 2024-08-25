import os

from dotenv import dotenv_values

TESTS_DIR = os.path.realpath(f"{os.path.dirname(__file__)}/..")
RESOURCE_DIR = f"{TESTS_DIR}/resource"
DEFAULT_TEST_ENV = dotenv_values(f"{TESTS_DIR}/test.env")
