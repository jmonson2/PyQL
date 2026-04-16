from typing import Any

from data.util.packer.impl.floatpacker import FloatPacker
from data.util.packer.impl.integerpacker import IntegerPacker
from data.util.packer.impl.stringpacker import StringPacker
from data.util.packer.packer import Packer


class PackerFactory:
    
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



