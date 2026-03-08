from enum import StrEnum, auto
from typing import List, Callable

class StrEnumBase(StrEnum):
    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def to_str(cls) -> str:
       return ', '.join([c.value for c in cls])

    def __str__(self) -> str:
        return self.value

class DocumentFormat(StrEnumBase):
    DICT        = auto()
    DICTCONFIG  = auto()
    YAML        = auto()
    JSON        = auto()
    TEXT        = auto()
    PDF         = auto()
    DOCX        = auto()
    HTML        = auto()
    MARKDOWN    = auto()
    DATAFRAME   = auto()
