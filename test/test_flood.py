import os
import time
import tempfile
import unittest

from src.storage.disk_manager import DiskManager
from src.storage.buffer_pool_manager import BufferPoolManager
from src.storage.table_heap import TableHeap
from src.record.types import TypeId
from src.record.column import Column
from src.record.schema import Schema
from src.record.tuple import Tuple

class TestFlood(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # Very small buffer pool (10 pages = 40KB in memory) 
        # This will force the BPM to evict to disk constantly when processing megabytes of data.
        self.dm = DiskManager(self.db_path)
        self.bpm = BufferPoolManager(pool_size=10, disk_manager=self.dm)
        
        # ~106 bytes per tuple
        self.schema = Schema([
            Column("id", TypeId.INTEGER),
            Column("data", TypeId.VARCHAR, 100) 
        ])

    def tearDown(self):
        self.dm.shut_down()
        os.remove(self.db_path)

    def test_flood_database(self):
        # 50,000 tuples * 114 bytes per slot = ~5.7 MB of data
        # Divided by 4096 bytes/page = ~1400 database pages.
        NUM_TUPLES = 50000 
        
        table_heap = TableHeap(self.bpm)
        
        print(f"\nStarting flood test with {NUM_TUPLES} tuples (~5.7 MB)...")
        print(f"Buffer pool is heavily constrained to 10 pages (40KB).")
        start_time = time.time()
        
        # 1. Insert Data
        for i in range(NUM_TUPLES):
            string_data = f"val_{i}".ljust(90, 'x')
            t = Tuple([i, string_data])
            serialized = t.serialize(self.schema)
            table_heap.insert_tuple(serialized)
            
            if i > 0 and i % 10000 == 0:
                print(f"Inserted {i} tuples...")
                
        insert_time = time.time() - start_time
        print(f"Insert phase completed in {insert_time:.2f} seconds.")
        
        # 2. Flush to disk and check file size
        self.bpm.flush_all_pages()
        file_size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
        print(f"Actual Database file size on disk: {file_size_mb:.2f} MB")
        
        # 3. Sequential Scan Retrieval
        print("Starting sequential scan retrieval...")
        start_time = time.time()
        
        count = 0
        for rid, tuple_data in table_heap.iterator():
            deserialized_tuple = Tuple(schema=self.schema, data=tuple_data)
            
            expected_id = count
            expected_str = f"val_{count}".ljust(90, 'x')
            
            self.assertEqual(deserialized_tuple.values[0], expected_id)
            self.assertEqual(deserialized_tuple.values[1], expected_str)
            
            count += 1
            if count % 10000 == 0:
                print(f"Successfully read and verified {count} tuples...")
                
        read_time = time.time() - start_time
        print(f"Read phase completed in {read_time:.2f} seconds.")
        
        self.assertEqual(count, NUM_TUPLES)
        print("Flood test completed successfully. The Buffer Pool Manager handled heavy eviction and paging flawlessly!")

if __name__ == '__main__':
    unittest.main()
