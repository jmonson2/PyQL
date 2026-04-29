import os
import json
from src.record.types import TypeId
from src.record.column import Column
from src.record.schema import Schema
from src.storage.buffer_pool_manager import BufferPoolManager
from src.storage.table_heap import TableHeap

class Catalog:
    """
    Catalog manages metadata for tables, associating table names 
    with their corresponding Schemas and physical TableHeaps.
    It persists this metadata in a simple JSON file so you can 
    read from tables created in previous sessions.
    """
    def __init__(self, catalog_path: str, bpm: BufferPoolManager):
        self.catalog_path = catalog_path
        self.bpm = bpm
        self.tables: dict[str, TableHeap] = {}
        self.schemas: dict[str, Schema] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.catalog_path):
            return
        
        with open(self.catalog_path, "r") as f:
            data = json.load(f)
            
        for table_name, table_info in data.items():
            cols = []
            for col in table_info["columns"]:
                cols.append(Column(col["name"], TypeId[col["type"]], col["length"]))
            self.schemas[table_name] = Schema(cols)
            # Link to existing table pages on disk
            self.tables[table_name] = TableHeap(self.bpm, table_info["first_page_id"])

    def _save(self) -> None:
        data = {}
        for table_name in self.tables:
            schema = self.schemas[table_name]
            first_page_id = self.tables[table_name].first_page_id
            cols = []
            for col in schema.columns:
                cols.append({
                    "name": col.column_name,
                    "type": col.column_type.name,
                    "length": col.max_length
                })
            data[table_name] = {
                "first_page_id": first_page_id,
                "columns": cols
            }
            
        with open(self.catalog_path, "w") as f:
            json.dump(data, f, indent=4)

    def create_table(self, table_name: str, schema: Schema) -> TableHeap:
        if table_name in self.tables:
            raise Exception(f"Table '{table_name}' already exists.")
        
        # This allocates a new page via the BufferPoolManager
        table_heap = TableHeap(self.bpm)
        
        self.tables[table_name] = table_heap
        self.schemas[table_name] = schema
        self._save()
        
        return table_heap

    def get_table(self, table_name: str) -> TableHeap:
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' does not exist.")
        return self.tables[table_name]

    def get_schema(self, table_name: str) -> Schema:
        if table_name not in self.schemas:
            raise Exception(f"Table '{table_name}' does not exist.")
        return self.schemas[table_name]
