from data.util.packer.impl.floatpacker import FloatPacker
from data.util.packer.impl.integerpacker import IntegerPacker
from data.util.packer.impl.stringpacker import StringPacker
from data.util.packer.packer import Packer


def main() -> None:
    packer: Packer = IntegerPacker()
    float_packer: FloatPacker = FloatPacker()
    string_packer: StringPacker = StringPacker()
    x = packer.pack(5)
    y = float_packer.pack(30.2159242768236487621)
    z = string_packer.pack("hello")
    print(x)

main()
