import struct

from data.util.packer.packer import Packer


class IntegerPacker(Packer):

    def pack(self, val: int) -> bytes:
        return struct.pack('<I', val)

    def unpack(self, val: bytes) -> int:
        return struct.unpack('<I', val)[0]