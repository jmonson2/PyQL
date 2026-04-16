from data.util.packer.impl.packerfactory import PackerFactory
from data.util.schema import Schema
from data.util.packer.packer import Packer

class BytesSchema(Schema):

    def __init__(self, schema: list[tuple[Packer, dict[bytes, bytes]]]):
        self.schema: list[tuple[Packer, dict[bytes, bytes]]] = schema

    def convert(self) -> dict[str, Schema.ImplementedTypes]:
        typed_schema: dict[str, Schema.ImplementedTypes] = {}
        for row in self.schema:
           key_packer: Packer = PackerFactory().get_packer("key")
           packer: Packer = row[0]
           data: dict[bytes, bytes] = row[1]
           for key, val in data.items():
               typed_schema[key_packer.unpack(key)] = packer.unpack(val)
        return typed_schema