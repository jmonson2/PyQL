import struct
from typing import Any

from data.util.serializer.serializer import Serializer


class StringSerializer(Serializer):
    def serialize(self, val: str) -> bytes:
        data: bytes = val.encode("utf-8")
        return struct.pack(f'<{len(data)}s', data)

    def deserialize(self, val: bytes) -> Any:
        return struct.unpack(f'<{len(val)}s', val)[0]