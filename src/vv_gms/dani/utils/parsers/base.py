from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterator

T = TypeVar("T")

class FileParser (ABC, Generic[T]):
    @abstractmethod
    def parse(self, filepath: str) -> Iterator[T]:
        pass