from src.record.types import TypeId

class Column:
    """
    Represents a column definition within a schema.
    """
    def __init__(self, column_name: str, column_type: TypeId, max_length: int = 0):
        self.column_name = column_name
        self.column_type = column_type
        # max_length is used primarily for VARCHAR types.
        self.max_length = max_length
        
        # calculate the fixed storage footprint of this column on a page
        self.fixed_length = self._calculate_fixed_length()

    def _calculate_fixed_length(self) -> int:
        if self.column_type == TypeId.INTEGER:
            return 4  # 4 bytes for a standard integer
        if self.column_type == TypeId.BOOLEAN:
            return 1  # 1 byte for boolean
        if self.column_type == TypeId.VARCHAR:
            # 2 bytes to store the actual length of the string, plus the max_length for the data
            return 2 + self.max_length
        return 0
