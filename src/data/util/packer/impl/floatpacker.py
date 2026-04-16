import struct

from data.util.packer.packer import Packer


class FloatPacker(Packer):

    def pack(self, val: float) -> bytes:
        return struct.pack('<f', val)

    def unpack(self, val: bytes) -> float:
        return struct.unpack('<f', val)[0]