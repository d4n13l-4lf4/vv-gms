import os
import tempfile
from typing import Callable, List, LiteralString

import pytest

from vv_gms.repositories.db import create_db


@pytest.fixture
def db():
    tmp_file = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=True)
    db = create_db(tmp_file.name)
    yield db
    tmp_file.close()

@pytest.fixture
def data_resolver() -> Callable[[list[str], str], str]:
    def __inner__(directories: List[str], file: str):
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, *directories, file)
        return str(config_path)
    return __inner__