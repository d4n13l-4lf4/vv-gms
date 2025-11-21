import os
from typing import Iterator, TypeVar

from vv_gms.dani.utils.mappers.dict import DictMapper
from vv_gms.dani.utils.parsers.base import FileParser

T = TypeVar("T")

class TXTParser(FileParser[T]):
    def __init__(self, converter: DictMapper[T]):
        self.__converter_ = converter

    def parse(self, filepath: str) -> Iterator[T]:
        with open(filepath, mode='r', newline='', encoding='utf-8') as txtfile:
            next(txtfile) # skip first header line
            for line in txtfile:
                fields = line.split(';')
                data = {idx: field.strip().strip(os.linesep) for idx, field in enumerate(fields)}
                yield self.__converter_.convert(data, 'txt')
