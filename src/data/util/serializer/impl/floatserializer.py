import struct

from data.util.serializer.serializer import Serializer


class FloatSerializer(Serializer):

    def serialize(self, val: float) -> bytes:
        return struct.pack('<f', val)

    def deserialize(self, val: bytes) -> float:
        return struct.unpack('<f', val)[0]