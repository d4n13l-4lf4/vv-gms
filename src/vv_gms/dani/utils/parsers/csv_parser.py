import csv
from typing import Iterator, TypeVar

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.utils.mappers.dict import DictMapper
from vv_gms.dani.utils.parsers.base import FileParser

T = TypeVar("T")

class CSVParser(FileParser[T]):
    def __init__(self, converter: DictMapper[T]):
        self.__converter_ = converter

    def parse(self, filepath: str) -> Iterator[T]:
        try:
            with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    yield self.__converter_.convert(row, 'csv')
        # Test case failed
        except Exception:
            raise CustomException('Invalid input type file, or arguments. Use: <CourseID> <CourseName>')