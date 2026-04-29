import struct
from typing import List, Any
from src.record.schema import Schema
from src.record.types import TypeId

class Tuple:
    """
    A Tuple represents a row of data in a table.
    It can serialize itself to bytes and deserialize from bytes using a Schema.
    """
    def __init__(self, values: List[Any] = None, schema: Schema = None, data: bytes | bytearray = None):
        """
        Initialize a Tuple. You can either provide a list of values,
        or provide raw bytes and a schema to deserialize.
        """
        if data is not None and schema is not None:
            self.values = self.deserialize(data, schema)
        else:
            self.values = values if values is not None else []

    def serialize(self, schema: Schema) -> bytearray:
        """
        Serialize the tuple's values into a bytearray according to the schema.
        """
        data = bytearray()
        for idx, col in enumerate(schema.columns):
            val = self.values[idx]
            
            if col.column_type == TypeId.INTEGER:
                # '<i' means little-endian standard integer (4 bytes)
                data.extend(struct.pack("<i", val))
                
            elif col.column_type == TypeId.BOOLEAN:
                # '<?' means little-endian boolean (1 byte)
                data.extend(struct.pack("<?", val))
                
            elif col.column_type == TypeId.VARCHAR:
                # For VARCHAR, we store the actual length (2 bytes), then the string, 
                # padded with null bytes to reach max_length.
                encoded = str(val).encode('utf-8')
                
                # Truncate if it exceeds max_length
                if len(encoded) > col.max_length:
                    encoded = encoded[:col.max_length]
                    
                # Write length as little-endian short (2 bytes)
                data.extend(struct.pack("<h", len(encoded)))
                
                # Write padded string
                data.extend(encoded.ljust(col.max_length, b'\x00'))
                
        return data

    @classmethod
    def deserialize(cls, data: bytes | bytearray, schema: Schema) -> List[Any]:
        """
        Deserialize raw bytes into a list of values based on the schema.
        """
        values = []
        offset = 0
        
        for col in schema.columns:
            if col.column_type == TypeId.INTEGER:
                val = struct.unpack_from("<i", data, offset)[0]
                values.append(val)
                offset += 4
                
            elif col.column_type == TypeId.BOOLEAN:
                val = struct.unpack_from("<?", data, offset)[0]
                values.append(val)
                offset += 1
                
            elif col.column_type == TypeId.VARCHAR:
                actual_len = struct.unpack_from("<h", data, offset)[0]
                offset += 2
                
                val_bytes = data[offset : offset + actual_len]
                values.append(val_bytes.decode('utf-8'))
                
                # Move offset past the padded section
                offset += col.max_length
                
        return values
