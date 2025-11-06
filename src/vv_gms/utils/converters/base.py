from dataclasses import fields
from typing import TypeVar, Type, Generic, Dict
from dacite import from_dict, Config

T = TypeVar("T")


def get_convert_key(cls: Type[T], meta_key: str):
    field_map = {f.name: f.metadata.get(meta_key, f.name) for f in fields(cls)}
    def __inner__(key: str) -> str:
        return field_map[key] if key in field_map else key
    return __inner__


class GenericConverter(Generic[T]):
    def __init__(self, cls: Type[T]):
        self.__cls_ = cls

    def convert(self, data, meta_key: str = 'plain') -> T:
        return from_dict(self.__cls_, data, Config(convert_key=get_convert_key(self.__cls_, meta_key)))
