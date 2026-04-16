from data.util.packer.impl.floatpacker import FloatPacker
from data.util.packer.impl.integerpacker import IntegerPacker
from data.util.packer.impl.stringpacker import StringPacker
from data.util.packer.packer import Packer
from data.util.typed_schema import TypedSchema
from data.util.bytes_schema import BytesSchema


def main() -> None:
   schema = {"id": 1, "temperature": 20.0, "day": "tuesday"}
   typed_schema = TypedSchema(schema)
   bytes_schema = typed_schema.convert()
   print(bytes_schema)
   typed_schema = BytesSchema(bytes_schema).convert()
   print(typed_schema)
main()
