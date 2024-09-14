import os
import shutil

import pytest
from helper import TEST_TEMP_DIR


@pytest.fixture(scope="session", autouse=True)
def create_tmp_directory():
    os.makedirs(TEST_TEMP_DIR, exist_ok=True)
    yield
    shutil.rmtree(TEST_TEMP_DIR, ignore_errors=True)
