import csv
from typing import Iterator, TypeVar

from vv_gms.utils.converters.base import GenericConverter
from vv_gms.utils.parsers.base import FileParser

T = TypeVar("T")

class GenericParser(FileParser[T]):
    def __init__(self, converter: GenericConverter[T]):
        self.__converter_ = converter

    def parse(self, filepath: str) -> Iterator[T]:
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield self.__converter_.convert(row)