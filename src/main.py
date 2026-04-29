import os
import sys
from src.parser.lexer import Lexer
from src.parser.parser import Parser
from src.storage.disk_manager import DiskManager
from src.storage.buffer_pool_manager import BufferPoolManager
from src.execution.catalog import Catalog
from src.execution.executor import Executor

def print_table(data):
    if not data:
        print("Empty set")
        return
        
    # Calculate column widths
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
    
    # Create format string
    fmt = " | ".join("{{:<{}}}".format(w) for w in col_widths)
    
    # Print separator and rows
    print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
    for i, row in enumerate(data):
        print(fmt.format(*row))
        if i == 0:
            print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
    print(f"({len(data) - 1} rows)")
    print()

def main():
    print("Welcome to PyQL!")
    print("Type '.exit' to exit.")
    print()
    
    # Use current working directory for DB files
    db_file = "pyql.db"
    catalog_file = "pyql_catalog.json"
    
    # Initialize Core Components
    dm = DiskManager(db_file)
    bpm = BufferPoolManager(pool_size=10, disk_manager=dm)
    catalog = Catalog(catalog_file, bpm)
    executor = Executor(catalog)
    
    # REPL Loop
    while True:
        try:
            query = input("pyql> ")
            if not query.strip():
                continue
            if query.strip().lower() == ".exit":
                break
                
            lexer = Lexer(query)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            statements = parser.parse()
            
            for stmt in statements:
                result = executor.execute(stmt)
                
                # Output handling
                if isinstance(result, str):
                    print(result)
                    print()
                elif isinstance(result, list):
                    print_table(result)
                        
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

    # Graceful shutdown
    print("Flushing buffer pool and shutting down...")
    bpm.flush_all_pages()
    dm.shut_down()
    print("Goodbye!")

if __name__ == "__main__":
    main()
