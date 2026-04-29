from enum import Enum

class TypeId(Enum):
    """Enumeration of supported data types in PyQL."""
    INVALID = 0
    BOOLEAN = 1
    INTEGER = 2
    VARCHAR = 3
