from data.util.serializer.impl.serializerfactory import SerializerFactory
from data.util.schema import Schema
from data.util.serializer.serializer import Serializer

class BytesSchema(Schema):

    def __init__(self, schema: list[tuple[Serializer, dict[bytes, bytes]]]):
        self.schema: list[tuple[Serializer, dict[bytes, bytes]]] = schema

    def convert(self) -> dict[str, Schema.ImplementedTypes]:
        typed_schema: dict[str, Schema.ImplementedTypes] = {}
        for row in self.schema:
           key_packer: Serializer = SerializerFactory().get_serializer("key")
           val_packer: Serializer = row[0]
           data: dict[bytes, bytes] = row[1]
           for key, val in data.items():
               typed_schema[key_packer.deserialize(key)] = val_packer.deserialize(val)
        return typed_schema