from platformdirs import PlatformDirs
from pathlib import Path

class PlatformPath:
    def __init__(self, dirs: PlatformDirs):
        self.__dirs_ = dirs
        self.__data_dir_ = Path(self.__dirs_.user_data_dir)
        self.__data_dir_.mkdir(parents=True, exist_ok=True)

    def get_user_data_filename(self, filename: str) -> str:
        return str(self.__data_dir_.joinpath(filename))