import unittest
import os
import tempfile

from src.storage.disk_manager import DiskManager
from src.storage.buffer_pool_manager import BufferPoolManager
from src.storage.table_heap import TableHeap
from src.record.types import TypeId
from src.record.column import Column
from src.record.schema import Schema
from src.record.tuple import Tuple

class TestTableHeap(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        self.dm = DiskManager(self.db_path)
        self.bpm = BufferPoolManager(5, self.dm)
        
        # Create schema: id INT, name VARCHAR(10)
        self.schema = Schema([
            Column("id", TypeId.INTEGER),
            Column("name", TypeId.VARCHAR, 10)
        ])

    def tearDown(self):
        self.dm.shut_down()
        os.remove(self.db_path)

    def test_table_heap_insertion_and_iteration(self):
        # Create a new TableHeap
        table_heap = TableHeap(self.bpm)
        
        # Insert 100 tuples
        for i in range(100):
            t = Tuple([i, f"Name_{i}"])
            data = t.serialize(self.schema)
            table_heap.insert_tuple(data)
            
        # Iterate over tuples and verify
        count = 0
        for rid, tuple_data in table_heap.iterator():
            deserialized_tuple = Tuple(schema=self.schema, data=tuple_data)
            
            self.assertEqual(deserialized_tuple.values[0], count)
            self.assertEqual(deserialized_tuple.values[1], f"Name_{count}")
            count += 1
            
        self.assertEqual(count, 100)

if __name__ == '__main__':
    unittest.main()
