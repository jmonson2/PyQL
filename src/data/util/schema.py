from data.util.packer.packer import Packer
from typing import Any
class Schema:
    bytes_schema: dict[Packer, dict[bytes, bytes]] | None
    typed_schema: dict[str, Any] | None

    def __init__(self, bytes_schema: dict[Packer, dict[bytes, bytes]] | None = None, typed_schema:dict[str, Any] | None = None):
       self.bytes_schema = bytes_schema
       self.typed_schema = typed_schema

    def pack_schema(self):
        pass
    def unpack_schema(self):
        pass