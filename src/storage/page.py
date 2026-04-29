from src.config import PAGE_SIZE, INVALID_PAGE_ID

class Page:
    """
    Page is the basic unit of storage within the database system.
    It represents a fixed-size block of memory (e.g., 4096 bytes)
    that acts as a container for physical data.
    """

    def __init__(self) -> None:
        """Initialize an empty page."""
        # The actual data contained within the page.
        # We use a bytearray for mutable sequence of bytes.
        self._data = bytearray(PAGE_SIZE)
        
        # The unique identifier for this page.
        self._page_id = INVALID_PAGE_ID
        
        # The number of threads/processes currently using this page.
        # A page cannot be evicted from the buffer pool if its pin_count > 0.
        self._pin_count = 0
        
        # A flag indicating whether the page has been modified since it was
        # read from disk. If True, it must be written back to disk before eviction.
        self._is_dirty = False

    def get_data(self) -> bytearray:
        """Get the raw byte data of the page."""
        return self._data

    def set_data(self, data: bytes | bytearray) -> None:
        """Set the raw byte data of the page. Must be exactly PAGE_SIZE bytes."""
        if len(data) != PAGE_SIZE:
            raise ValueError(f"Data length must be exactly {PAGE_SIZE} bytes.")
        self._data = bytearray(data)

    def get_page_id(self) -> int:
        """Get the ID of this page."""
        return self._page_id

    def set_page_id(self, page_id: int) -> None:
        """Set the ID of this page."""
        self._page_id = page_id

    def get_pin_count(self) -> int:
        """Get the current pin count."""
        return self._pin_count

    def pin(self) -> None:
        """Increment the pin count."""
        self._pin_count += 1

    def unpin(self) -> None:
        """Decrement the pin count."""
        if self._pin_count > 0:
            self._pin_count -= 1

    def is_dirty(self) -> bool:
        """Check if the page is dirty."""
        return self._is_dirty

    def set_dirty(self, is_dirty: bool) -> None:
        """Set the dirty flag for the page."""
        self._is_dirty = is_dirty

    def reset_memory(self) -> None:
        """Reset the page to an uninitialized state."""
        self._data = bytearray(PAGE_SIZE)
        self._page_id = INVALID_PAGE_ID
        self._pin_count = 0
        self._is_dirty = False
