import struct

from data.util.serializer.serializer import Serializer


class IntegerSerializer(Serializer):

    def serialize(self, val: int) -> bytes:
        return struct.pack('<I', val)

    def deserialize(self, val: bytes) -> int:
        return struct.unpack('<I', val)[0]