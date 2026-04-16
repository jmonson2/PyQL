from typing import Protocol, Any


class Packer(Protocol):
    def __init__(self):
        pass

    def pack(self, val: Any) -> bytes: ...
    def unpack(self, val: bytes) -> Any: ...