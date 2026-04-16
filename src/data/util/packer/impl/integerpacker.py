from data.util.packer.packer import Packer
import struct

class IntegerPacker(Packer):

    def __init__(self):
        super().__init__()

    def pack(self, val: int) -> bytes:
        return struct.pack('<I', val)

    def unpack(self, val: bytes) -> int:
        return struct.unpack('<I', val)[0]