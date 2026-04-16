from data.util.packer.packer import Packer
from data.util.packer.impl.packerfactory import PackerFactory
from data.util.schema import Schema
from typing import Any, TypeAlias
class TypedSchema(Schema):
    schema: dict[str, Schema.ImplementedTypes]

    def __init__(self, schema: dict[str, Schema.ImplementedTypes]):
        self.schema = schema
        self.packer_factory: PackerFactory = PackerFactory()

    def convert(self) -> list[tuple[Packer, dict[bytes, bytes]]]:
        bytes_schema: list[tuple[Packer, dict[bytes, bytes]]] = []
        for key, val in self.schema.items():
            key_packer: Packer = self.packer_factory.get_packer(key) #key_packer should always be a str
            val_packer: Packer = self.packer_factory.get_packer(val)
            bytes_schema.append((val_packer, {key_packer.pack(key): val_packer.pack(val)}))
        return bytes_schema

    def unpack_schema(self):
        pass
