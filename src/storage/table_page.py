import struct
from src.config import PAGE_SIZE, INVALID_PAGE_ID
from src.storage.page import Page
from typing import Optional

class TablePage:
    """
    TablePage provides a slotted-page abstraction over a raw Page object.
    
    Header format (20 bytes):
    - page_id (4 bytes, integer)
    - prev_page_id (4 bytes, integer)
    - next_page_id (4 bytes, integer)
    - free_space_pointer (4 bytes, integer)
    - slot_count (4 bytes, integer)
    
    Slots grow from the top (offset 20) downwards.
    Data grows from the bottom (PAGE_SIZE) upwards.
    """
    HEADER_SIZE = 20
    SLOT_SIZE = 8  # 4 bytes for tuple offset, 4 bytes for tuple size

    def __init__(self, page: Page):
        self.page = page

    def init(self, page_id: int, prev_page_id: int = INVALID_PAGE_ID) -> None:
        """Initialize the header of a new page."""
        self.page.set_page_id(page_id)
        data = self.page.get_data()
        next_page_id = INVALID_PAGE_ID
        free_space_pointer = PAGE_SIZE
        slot_count = 0
        struct.pack_into("<iiiii", data, 0, page_id, prev_page_id, next_page_id, free_space_pointer, slot_count)
        self.page.set_dirty(True)

    def get_page_id(self) -> int:
        return struct.unpack_from("<i", self.page.get_data(), 0)[0]

    def get_prev_page_id(self) -> int:
        return struct.unpack_from("<i", self.page.get_data(), 4)[0]

    def get_next_page_id(self) -> int:
        return struct.unpack_from("<i", self.page.get_data(), 8)[0]

    def set_next_page_id(self, next_page_id: int) -> None:
        struct.pack_into("<i", self.page.get_data(), 8, next_page_id)
        self.page.set_dirty(True)

    def get_free_space_pointer(self) -> int:
        return struct.unpack_from("<i", self.page.get_data(), 12)[0]

    def set_free_space_pointer(self, ptr: int) -> None:
        struct.pack_into("<i", self.page.get_data(), 12, ptr)
        self.page.set_dirty(True)

    def get_slot_count(self) -> int:
        return struct.unpack_from("<i", self.page.get_data(), 16)[0]

    def set_slot_count(self, count: int) -> None:
        struct.pack_into("<i", self.page.get_data(), 16, count)
        self.page.set_dirty(True)

    def get_free_space_remaining(self) -> int:
        return self.get_free_space_pointer() - (self.HEADER_SIZE + self.get_slot_count() * self.SLOT_SIZE)

    def insert_tuple(self, tuple_data: bytes | bytearray) -> Optional[int]:
        """
        Inserts a tuple into the page if there is enough space.
        Returns the slot index if successful, or None if not enough space.
        """
        size = len(tuple_data)
        if self.get_free_space_remaining() < size + self.SLOT_SIZE:
            return None

        # Allocate space from the end (bottom-up)
        free_space_ptr = self.get_free_space_pointer()
        new_ptr = free_space_ptr - size
        self.set_free_space_pointer(new_ptr)

        # Write tuple data
        data = self.page.get_data()
        data[new_ptr : new_ptr + size] = tuple_data

        # Write slot entry (offset, size) from top-down
        slot_idx = self.get_slot_count()
        slot_offset = self.HEADER_SIZE + slot_idx * self.SLOT_SIZE
        struct.pack_into("<ii", data, slot_offset, new_ptr, size)

        self.set_slot_count(slot_idx + 1)
        self.page.set_dirty(True)

        return slot_idx

    def get_tuple(self, slot_idx: int) -> Optional[bytearray]:
        """Reads a tuple's raw bytes given its slot index."""
        if slot_idx < 0 or slot_idx >= self.get_slot_count():
            return None
        
        slot_offset = self.HEADER_SIZE + slot_idx * self.SLOT_SIZE
        tuple_offset, tuple_size = struct.unpack_from("<ii", self.page.get_data(), slot_offset)
        
        # A deleted tuple might have a size of 0
        if tuple_size == 0:
            return None

        return self.page.get_data()[tuple_offset : tuple_offset + tuple_size]
