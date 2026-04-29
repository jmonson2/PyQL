import unittest
from src.parser.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast import CreateTableStatement, InsertStatement, SelectStatement

class TestParser(unittest.TestCase):
    def parse_text(self, text: str):
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_create_table(self):
        text = "CREATE TABLE users (id INTEGER, name VARCHAR(20), is_active BOOLEAN);"
        statements = self.parse_text(text)
        
        self.assertEqual(len(statements), 1)
        stmt = statements[0]
        self.assertIsInstance(stmt, CreateTableStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(len(stmt.columns), 3)
        
        self.assertEqual(stmt.columns[0].name, "id")
        self.assertEqual(stmt.columns[0].data_type, "INTEGER")
        
        self.assertEqual(stmt.columns[1].name, "name")
        self.assertEqual(stmt.columns[1].data_type, "VARCHAR")
        self.assertEqual(stmt.columns[1].length, 20)
        
        self.assertEqual(stmt.columns[2].name, "is_active")
        self.assertEqual(stmt.columns[2].data_type, "BOOLEAN")

    def test_insert(self):
        text = "INSERT INTO users VALUES (1, 'Alice', TRUE);"
        statements = self.parse_text(text)
        
        self.assertEqual(len(statements), 1)
        stmt = statements[0]
        self.assertIsInstance(stmt, InsertStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.values, [1, "Alice", True])

    def test_select(self):
        text = "SELECT id, name FROM users;"
        statements = self.parse_text(text)
        
        self.assertEqual(len(statements), 1)
        stmt = statements[0]
        self.assertIsInstance(stmt, SelectStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.columns, ["id", "name"])

    def test_select_star(self):
        text = "SELECT * FROM users"
        statements = self.parse_text(text)
        
        self.assertEqual(len(statements), 1)
        stmt = statements[0]
        self.assertIsInstance(stmt, SelectStatement)
        self.assertEqual(stmt.table_name, "users")
        self.assertEqual(stmt.columns, ["*"])

    def test_multiple_statements(self):
        text = "CREATE TABLE a (id INT); INSERT INTO a VALUES (1); SELECT * FROM a;"
        statements = self.parse_text(text)
        self.assertEqual(len(statements), 3)
        self.assertIsInstance(statements[0], CreateTableStatement)
        self.assertIsInstance(statements[1], InsertStatement)
        self.assertIsInstance(statements[2], SelectStatement)

if __name__ == '__main__':
    unittest.main()
