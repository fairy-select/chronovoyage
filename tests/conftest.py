import os

from dotenv import dotenv_values

TESTS_DIR = os.path.dirname(__file__)

DEFAULT_TEST_ENV = dotenv_values(f"{TESTS_DIR}/test.env")
