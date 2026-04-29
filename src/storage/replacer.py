from typing import Optional

class LRUReplacer:
    """
    LRUReplacer implements the Least Recently Used replacement policy.
    It tracks frame IDs that are currently unpinned and available for eviction.
    """

    def __init__(self, num_pages: int):
        """
        Initialize the LRUReplacer.
        
        Args:
            num_pages (int): The maximum number of pages (frames) the replacer will track.
        """
        self._capacity = num_pages
        # Python 3.7+ dictionaries maintain insertion order.
        # We use it as an ordered set.
        self._lru_cache: dict[int, None] = {}

    def victim(self) -> Optional[int]:
        """
        Remove and return the victim frame.
        The victim is the least recently unpinned frame.

        Returns:
            Optional[int]: The frame ID of the victim, or None if no frames are available.
        """
        if not self._lru_cache:
            return None
            
        # Get the first key (least recently inserted)
        frame_id = next(iter(self._lru_cache))
        del self._lru_cache[frame_id]
        return frame_id

    def pin(self, frame_id: int) -> None:
        """
        Pin a frame, indicating it is currently in use.
        This removes the frame from the replacer, protecting it from eviction.

        Args:
            frame_id (int): The ID of the frame to pin.
        """
        if frame_id in self._lru_cache:
            del self._lru_cache[frame_id]

    def unpin(self, frame_id: int) -> None:
        """
        Unpin a frame, indicating it is no longer in use.
        This adds the frame to the replacer if it's not already there.

        Args:
            frame_id (int): The ID of the frame to unpin.
        """
        if frame_id not in self._lru_cache:
            self._lru_cache[frame_id] = None

    def size(self) -> int:
        """
        Return the number of frames currently tracked by the replacer.
        
        Returns:
            int: The number of unpinned frames.
        """
        return len(self._lru_cache)
