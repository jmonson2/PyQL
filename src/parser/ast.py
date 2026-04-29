class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    pass

class ColumnDef(ASTNode):
    def __init__(self, name: str, data_type: str, length: int = 0):
        self.name = name
        self.data_type = data_type
        self.length = length

    def __repr__(self):
        if self.length > 0:
            return f"{self.name} {self.data_type}({self.length})"
        return f"{self.name} {self.data_type}"

class CreateTableStatement(ASTNode):
    def __init__(self, table_name: str, columns: list[ColumnDef]):
        self.table_name = table_name
        self.columns = columns

    def __repr__(self):
        cols = ", ".join(repr(c) for c in self.columns)
        return f"CREATE TABLE {self.table_name} ({cols})"

class InsertStatement(ASTNode):
    def __init__(self, table_name: str, values: list):
        self.table_name = table_name
        self.values = values

    def __repr__(self):
        vals = ", ".join(repr(v) for v in self.values)
        return f"INSERT INTO {self.table_name} VALUES ({vals})"

class SelectStatement(ASTNode):
    def __init__(self, table_name: str, columns: list[str] = None):
        self.table_name = table_name
        self.columns = columns if columns else ["*"]

    def __repr__(self):
        cols = ", ".join(self.columns)
        return f"SELECT {cols} FROM {self.table_name}"
