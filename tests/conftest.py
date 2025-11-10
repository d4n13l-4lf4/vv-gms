import os
from typing import Callable, List

import pytest

@pytest.fixture
def get_filename() -> Callable[[str], str]:
    def __inner__(file: str):
        dir_to_search = ['resources', 'data']
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, *dir_to_search, file)
        return str(config_path)
    return __inner__