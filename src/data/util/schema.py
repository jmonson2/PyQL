from typing import Protocol
from data.util.packer.impl.packerfactory import PackerFactory
class Schema(Protocol):

    type ImplementedTypes = int | float | str
    def convert(self): ...
