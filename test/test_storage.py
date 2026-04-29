import unittest
import os
import tempfile
from src.config import PAGE_SIZE
from src.storage.disk_manager import DiskManager
from src.storage.buffer_pool_manager import BufferPoolManager

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name

    def tearDown(self):
        os.remove(self.db_path)

    def test_buffer_pool_manager(self):
        dm = DiskManager(self.db_path)
        bpm = BufferPoolManager(3, dm)  # Pool size of 3

        # Create a new page
        page0 = bpm.new_page()
        self.assertIsNotNone(page0)
        self.assertEqual(page0.get_page_id(), 0)

        # Write some data to page 0
        data = bytearray(b"Hello World".ljust(PAGE_SIZE, b'\x00'))
        page0.set_data(data)
        
        # Unpin page 0, mark as dirty
        bpm.unpin_page(0, is_dirty=True)

        # Create 3 more pages to force eviction of page 0
        page1 = bpm.new_page()
        bpm.unpin_page(1, is_dirty=False)
        
        page2 = bpm.new_page()
        bpm.unpin_page(2, is_dirty=False)

        page3 = bpm.new_page()
        bpm.unpin_page(3, is_dirty=False)

        # Fetch page 0 back into memory
        fetched_page0 = bpm.fetch_page(0)
        self.assertIsNotNone(fetched_page0)
        self.assertEqual(fetched_page0.get_data()[:11], b"Hello World")
        bpm.unpin_page(0, is_dirty=False)

        dm.shut_down()

if __name__ == '__main__':
    unittest.main()
