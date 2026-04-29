from typing import Iterator, Tuple as PyTuple
from src.storage.buffer_pool_manager import BufferPoolManager
from src.storage.table_page import TablePage
from src.config import INVALID_PAGE_ID

class RecordId:
    """
    RecordId uniquely identifies a tuple within the database 
    by its page ID and its slot index on that page.
    """
    def __init__(self, page_id: int, slot_idx: int):
        self.page_id = page_id
        self.slot_idx = slot_idx

    def __repr__(self):
        return f"RecordId({self.page_id}, {self.slot_idx})"


class TableHeap:
    """
    TableHeap manages a doubly linked list of TablePages.
    It represents the physical storage of a table.
    """
    def __init__(self, bpm: BufferPoolManager, first_page_id: int = INVALID_PAGE_ID):
        self.bpm = bpm
        
        if first_page_id == INVALID_PAGE_ID:
            # Create the very first page
            first_page = self.bpm.new_page()
            if first_page is None:
                raise Exception("Out of memory/disk space when creating table heap.")
            
            self.first_page_id = first_page.get_page_id()
            table_page = TablePage(first_page)
            table_page.init(self.first_page_id)
            self.bpm.unpin_page(self.first_page_id, is_dirty=True)
        else:
            self.first_page_id = first_page_id

    def insert_tuple(self, tuple_data: bytes | bytearray) -> RecordId:
        """
        Insert a serialized tuple into the table.
        It finds the first page with enough free space. If none, allocates a new page.
        """
        curr_page_id = self.first_page_id
        
        while curr_page_id != INVALID_PAGE_ID:
            page = self.bpm.fetch_page(curr_page_id)
            if page is None:
                raise Exception(f"Failed to fetch page {curr_page_id}")
                
            table_page = TablePage(page)
            
            # Try to insert
            slot_idx = table_page.insert_tuple(tuple_data)
            
            if slot_idx is not None:
                # Successfully inserted!
                self.bpm.unpin_page(curr_page_id, is_dirty=True)
                return RecordId(curr_page_id, slot_idx)
            
            # Not enough space on this page, move to the next page
            next_page_id = table_page.get_next_page_id()
            
            if next_page_id == INVALID_PAGE_ID:
                # Reached the end of the heap. Need to allocate a new page.
                new_page = self.bpm.new_page()
                if new_page is None:
                    raise Exception("Out of memory/disk space when appending to table heap.")
                    
                new_page_id = new_page.get_page_id()
                new_table_page = TablePage(new_page)
                new_table_page.init(new_page_id, prev_page_id=curr_page_id)
                
                # Update next pointer of current page
                table_page.set_next_page_id(new_page_id)
                
                # Insert into the new page (assuming it definitely fits if it's smaller than PAGE_SIZE)
                slot_idx = new_table_page.insert_tuple(tuple_data)
                
                self.bpm.unpin_page(new_page_id, is_dirty=True)
                self.bpm.unpin_page(curr_page_id, is_dirty=True)
                
                return RecordId(new_page_id, slot_idx)
            
            self.bpm.unpin_page(curr_page_id, is_dirty=False)
            curr_page_id = next_page_id
            
        raise Exception("Failed to insert tuple.")

    def iterator(self) -> Iterator[PyTuple[RecordId, bytearray]]:
        """
        Iterate through all tuples in the table heap.
        Yields (RecordId, tuple_data_bytes).
        """
        curr_page_id = self.first_page_id
        
        while curr_page_id != INVALID_PAGE_ID:
            page = self.bpm.fetch_page(curr_page_id)
            if page is None:
                break
                
            table_page = TablePage(page)
            
            slot_count = table_page.get_slot_count()
            for slot_idx in range(slot_count):
                tuple_data = table_page.get_tuple(slot_idx)
                if tuple_data is not None:
                    yield RecordId(curr_page_id, slot_idx), tuple_data
            
            next_page_id = table_page.get_next_page_id()
            self.bpm.unpin_page(curr_page_id, is_dirty=False)
            curr_page_id = next_page_id
