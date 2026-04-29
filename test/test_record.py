import unittest
from src.record.types import TypeId
from src.record.column import Column
from src.record.schema import Schema
from src.record.tuple import Tuple

class TestRecord(unittest.TestCase):
    def test_tuple_serialization(self):
        # 1. Define a schema
        # id: INTEGER, is_active: BOOLEAN, name: VARCHAR(10)
        col1 = Column("id", TypeId.INTEGER)
        col2 = Column("is_active", TypeId.BOOLEAN)
        col3 = Column("name", TypeId.VARCHAR, max_length=10)
        
        schema = Schema([col1, col2, col3])
        
        # Check schema length
        # INTEGER(4) + BOOLEAN(1) + VARCHAR(2 + 10) = 17 bytes
        self.assertEqual(schema.length, 17)
        
        # 2. Create a tuple
        original_values = [42, True, "Alice"]
        t = Tuple(original_values)
        
        # 3. Serialize
        data = t.serialize(schema)
        self.assertEqual(len(data), 17)
        
        # 4. Deserialize
        deserialized_tuple = Tuple(schema=schema, data=data)
        
        # 5. Verify
        self.assertEqual(deserialized_tuple.values[0], 42)
        self.assertEqual(deserialized_tuple.values[1], True)
        self.assertEqual(deserialized_tuple.values[2], "Alice")

    def test_varchar_truncation(self):
        col = Column("name", TypeId.VARCHAR, max_length=5)
        schema = Schema([col])
        
        # "LongName" is 8 characters, should be truncated to 5
        t = Tuple(["LongName"])
        data = t.serialize(schema)
        
        t2 = Tuple(schema=schema, data=data)
        self.assertEqual(t2.values[0], "LongN")

if __name__ == '__main__':
    unittest.main()
