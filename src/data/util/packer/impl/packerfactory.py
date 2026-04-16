from typing import Any
from data.util.packer.packer import Packer
from data.util.packer.impl.floatpacker import FloatPacker
from data.util.packer.impl.integerpacker import IntegerPacker
from data.util.packer.impl.stringpacker import StringPacker

class PackerFactory:
    
    def __init__(self):
        pass

    @staticmethod
    def get_packer(val: Any) -> Packer:
            match val:
                case int():
                    return IntegerPacker()
                case float():
                    return FloatPacker()
                case str():
                    return StringPacker()

            raise ValueError("Invalid data type")



