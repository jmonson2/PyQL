import struct
from typing import Any

from data.util.packer.packer import Packer


class StringPacker(Packer):
    def pack(self, val: str) -> bytes:
        data: bytes = val.encode("utf-8")
        return struct.pack(f'<{len(data)}s', data)

    def unpack(self, val: bytes) -> Any:
        return struct.unpack(f'<{len(val)}s', val)[0]