from typing import List
from src.record.column import Column

class Schema:
    """
    A schema defines the structure of a table or a tuple, 
    consisting of a list of columns.
    """
    def __init__(self, columns: List[Column]):
        self.columns = columns
        # The total size in bytes of a tuple using this schema
        self.length = sum(col.fixed_length for col in columns)
        
    def get_column(self, col_idx: int) -> Column:
        """Get the column at the specified index."""
        return self.columns[col_idx]
        
    def get_column_count(self) -> int:
        """Get the number of columns in the schema."""
        return len(self.columns)
