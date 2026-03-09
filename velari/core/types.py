from enum import StrEnum, auto
from typing import List, Callable

class StrEnumBase(StrEnum):
    """Extend StrEnum with helpers to expose member names and values as lists or strings."""

    @classmethod
    def list_names(cls) -> List[str]:
        """Return all member names as a list of strings."""
        return list(map(lambda c: c.name, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        """Return all member values as a list of strings."""
        return list(map(lambda c: c.value, cls))

    @classmethod
    def to_str(cls) -> str:
        """Return a comma-separated string of all member values."""
        return ', '.join([c.value for c in cls])

    def __str__(self) -> str:
        return self.value

class DocumentFormat(StrEnumBase):
    """Enumerate supported document and data serialisation formats."""

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
