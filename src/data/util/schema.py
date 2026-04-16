from typing import Protocol


class Schema(Protocol):

    type ImplementedTypes = int | float | str
    def convert(self): ...
