from data.util.serializer.impl.serializerfactory import SerializerFactory
from data.util.serializer.serializer import Serializer
from data.util.schema import Schema


class TypedSchema(Schema):
    schema: dict[str, Schema.ImplementedTypes]

    def __init__(self, schema: dict[str, Schema.ImplementedTypes]):
        self.schema = schema
        self.packer_factory: SerializerFactory = SerializerFactory()

    def convert(self) -> list[tuple[Serializer, dict[bytes, bytes]]]:
        bytes_schema: list[tuple[Serializer, dict[bytes, bytes]]] = []
        for key, val in self.schema.items():
            key_packer: Serializer = self.packer_factory.get_serializer(key) #key_packer should always be a str
            val_packer: Serializer = self.packer_factory.get_serializer(val)
            bytes_schema.append((val_packer, {key_packer.serialize(key): val_packer.serialize(val)}))
        return bytes_schema

    def unpack_schema(self):
        pass
