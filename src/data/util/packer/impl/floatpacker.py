import struct
from data.util.packer.packer import Packer

class FloatPacker(Packer):

    def __init__(self):
        super().__init__()

    def pack(self, val: float) -> bytes:
        return struct.pack('<f', val)

    def unpack(self, val: bytes) -> float:
        return struct.unpack('<f', val)[0]