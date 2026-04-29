from typing import Optional
from src.config import INVALID_PAGE_ID
from src.storage.page import Page
from src.storage.disk_manager import DiskManager
from src.storage.replacer import LRUReplacer

class BufferPoolManager:
    """
    BufferPoolManager is responsible for moving pages between memory (the buffer pool)
    and disk (the database file). It integrates the DiskManager and a Replacer.
    """

    def __init__(self, pool_size: int, disk_manager: DiskManager):
        """
        Initialize the BufferPoolManager.

        Args:
            pool_size (int): The maximum number of pages in memory at once.
            disk_manager (DiskManager): The manager responsible for disk I/O.
        """
        self._pool_size = pool_size
        self._disk_manager = disk_manager
        self._replacer = LRUReplacer(pool_size)

        # The array of pages in memory (the buffer pool itself)
        self._pages = [Page() for _ in range(pool_size)]
        
        # Maps page_id to frame_id (the index in the _pages array)
        self._page_table: dict[int, int] = {}
        
        # List of frames that are currently unused and have no valid page in them
        self._free_list = list(range(pool_size))

    def _find_available_frame(self) -> Optional[int]:
        """
        Helper method to find a free frame or evict a victim.
        If a victim is evicted and it is dirty, it is written to disk.
        
        Returns:
            Optional[int]: The frame_id of an available frame, or None if all are pinned.
        """
        # Option 1: Pick from the free list
        if self._free_list:
            return self._free_list.pop(0)

        # Option 2: Ask replacer for a victim
        victim_frame = self._replacer.victim()
        if victim_frame is None:
            return None  # All pages are pinned

        # We found a victim. Check if it's dirty and needs to be flushed.
        victim_page = self._pages[victim_frame]
        if victim_page.is_dirty():
            self._disk_manager.write_page(victim_page.get_page_id(), victim_page.get_data())
            victim_page.set_dirty(False)

        # Remove the victim from the page table
        if victim_page.get_page_id() != INVALID_PAGE_ID:
            del self._page_table[victim_page.get_page_id()]

        return victim_frame

    def fetch_page(self, page_id: int) -> Optional[Page]:
        """
        Fetch a page from the buffer pool. If it's not in memory, read it from disk.
        This implicitly pins the page.

        Args:
            page_id (int): The ID of the page to fetch.

        Returns:
            Optional[Page]: The requested page, or None if no frames are available.
        """
        # Case 1: Page is already in memory
        if page_id in self._page_table:
            frame_id = self._page_table[page_id]
            page = self._pages[frame_id]
            page.pin()
            self._replacer.pin(frame_id)
            return page

        # Case 2: Page is not in memory. Find an available frame.
        frame_id = self._find_available_frame()
        if frame_id is None:
            return None

        # Read the page from disk into the frame
        page = self._pages[frame_id]
        page_data = self._disk_manager.read_page(page_id)
        
        page.set_data(page_data)
        page.set_page_id(page_id)
        page.reset_memory() # resets pins/dirty, but clears data! Wait, don't do this.
        
        # Proper initialization of the page object
        page.set_page_id(page_id)
        page._pin_count = 1
        page.set_dirty(False)
        page.set_data(page_data)

        # Update metadata
        self._page_table[page_id] = frame_id
        self._replacer.pin(frame_id)

        return page

    def new_page(self) -> Optional[Page]:
        """
        Create a new page in the database file and fetch it into the buffer pool.
        This implicitly pins the new page.

        Returns:
            Optional[Page]: The new page, or None if no frames are available.
        """
        frame_id = self._find_available_frame()
        if frame_id is None:
            return None

        # Allocate a new page on disk
        new_page_id = self._disk_manager.allocate_page()
        
        page = self._pages[frame_id]
        page.set_page_id(new_page_id)
        page._pin_count = 1
        page.set_dirty(False)
        page._data = bytearray(self._disk_manager.read_page(new_page_id)) # Initialize with empty data

        self._page_table[new_page_id] = frame_id
        self._replacer.pin(frame_id)

        return page

    def unpin_page(self, page_id: int, is_dirty: bool = False) -> bool:
        """
        Unpin a page, indicating the caller is done using it.

        Args:
            page_id (int): The ID of the page to unpin.
            is_dirty (bool): Whether the caller modified the page.

        Returns:
            bool: True if the page was successfully unpinned, False if it was not in the pool or already fully unpinned.
        """
        if page_id not in self._page_table:
            return False

        frame_id = self._page_table[page_id]
        page = self._pages[frame_id]

        if page.get_pin_count() <= 0:
            return False

        page.unpin()
        if is_dirty:
            page.set_dirty(True)

        # If this was the last thread using the page, add it to the replacer
        if page.get_pin_count() == 0:
            self._replacer.unpin(frame_id)

        return True

    def flush_page(self, page_id: int) -> bool:
        """
        Force flush a page to disk regardless of its pin count or replacer state.

        Args:
            page_id (int): The ID of the page to flush.

        Returns:
            bool: True if successful, False if the page was not found.
        """
        if page_id not in self._page_table:
            return False

        frame_id = self._page_table[page_id]
        page = self._pages[frame_id]
        
        self._disk_manager.write_page(page_id, page.get_data())
        page.set_dirty(False)
        return True

    def flush_all_pages(self) -> None:
        """Flush all valid pages in the buffer pool to disk."""
        for page_id in list(self._page_table.keys()):
            self.flush_page(page_id)
