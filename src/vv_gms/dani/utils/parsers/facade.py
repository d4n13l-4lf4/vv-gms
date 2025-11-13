from typing import TypeVar, Iterator

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.utils.parsers.base import FileParser

T = TypeVar('T')

class FacadeParser(FileParser[T]):
    def __init__(self, txt_parser: FileParser[T], csv_parser: FileParser[T]):
        self.__csv_parser_ = csv_parser
        self.__txt_parser_ = txt_parser

    def parse(self, filepath: str) -> Iterator[T]:
        if filepath.endswith('.csv'):
            return self.__csv_parser_.parse(filepath)
        if filepath.endswith('.txt'):
            return self.__txt_parser_.parse(filepath)
        raise CustomException('Invalid input type file, or arguments. Use: <CourseID> <CourseName>')