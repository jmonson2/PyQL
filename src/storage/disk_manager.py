import os
from src.config import PAGE_SIZE

class DiskManager:
    """
    DiskManager handles reading and writing database pages to and from the physical file.
    """

    def __init__(self, db_file: str) -> None:
        """
        Initialize the DiskManager.

        Args:
            db_file (str): The path to the database file.
        """
        self._file_name = db_file
        self._next_page_id = 0
        
        # Open file in read/write binary mode. Create it if it doesn't exist.
        if not os.path.exists(self._file_name):
            self._file = open(self._file_name, 'wb+')
        else:
            self._file = open(self._file_name, 'rb+')

        # Determine the next available page ID based on file size
        self._file.seek(0, os.SEEK_END)
        file_size = self._file.tell()
        self._next_page_id = file_size // PAGE_SIZE

    def shut_down(self) -> None:
        """Close the underlying file stream."""
        if self._file and not self._file.closed:
            self._file.close()

    def write_page(self, page_id: int, page_data: bytes | bytearray) -> None:
        """
        Write a page to the database file.

        Args:
            page_id (int): The ID of the page to write.
            page_data (bytes | bytearray): The raw data to write. Must be PAGE_SIZE bytes.
        """
        if len(page_data) != PAGE_SIZE:
            raise ValueError(f"Data to write must be exactly {PAGE_SIZE} bytes.")
            
        offset = page_id * PAGE_SIZE
        self._file.seek(offset)
        self._file.write(page_data)
        self._file.flush()

    def read_page(self, page_id: int) -> bytearray:
        """
        Read a page from the database file.

        Args:
            page_id (int): The ID of the page to read.

        Returns:
            bytearray: A bytearray containing the page data.
        """
        if page_id >= self._next_page_id or page_id < 0:
            raise ValueError("Invalid page ID or page not allocated.")
            
        offset = page_id * PAGE_SIZE
        self._file.seek(offset)
        data = self._file.read(PAGE_SIZE)
        
        # If the file is somehow shorter than expected, pad it with zeros
        if len(data) < PAGE_SIZE:
            data = data.ljust(PAGE_SIZE, b'\x00')
            
        return bytearray(data)

    def allocate_page(self) -> int:
        """
        Allocate a new page.

        Returns:
            int: The new page ID.
        """
        new_page_id = self._next_page_id
        self._next_page_id += 1
        return new_page_id

    def deallocate_page(self, page_id: int) -> None:
        """
        Deallocate a page (no-op for now).
        In a more advanced implementation, this would track free pages
        to reuse them in future allocations.
        """
        pass
