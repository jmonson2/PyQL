import unittest
import sys
import os

# Add src to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from parser import Lexer, TokenType, LexerError

class TestLexer(unittest.TestCase):
    def test_basic_select(self):
        sql = "SELECT id, name FROM users;"
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        
        expected = [
            (TokenType.SELECT, "SELECT"),
            (TokenType.IDENTIFIER, "id"),
            (TokenType.COMMA, ","),
            (TokenType.IDENTIFIER, "name"),
            (TokenType.FROM, "FROM"),
            (TokenType.IDENTIFIER, "users"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.EOF, "")
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for token, (exp_type, exp_val) in zip(tokens, expected):
            self.assertEqual(token.type, exp_type)
            self.assertEqual(token.value, exp_val)

    def test_literals_and_conditions(self):
        sql = "WHERE age = 25 AND status = 'active'"
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        
        expected = [
            (TokenType.WHERE, "WHERE"),
            (TokenType.IDENTIFIER, "age"),
            (TokenType.EQUALS, "="),
            (TokenType.NUMBER_LITERAL, "25"),
            (TokenType.AND, "AND"),
            (TokenType.IDENTIFIER, "status"),
            (TokenType.EQUALS, "="),
            (TokenType.STRING_LITERAL, "'active'"),
            (TokenType.EOF, "")
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for token, (exp_type, exp_val) in zip(tokens, expected):
            self.assertEqual(token.type, exp_type)
            self.assertEqual(token.value, exp_val)

    def test_illegal_character(self):
        sql = "SELECT @name;"
        lexer = Lexer(sql)
        with self.assertRaises(LexerError):
            lexer.tokenize()

if __name__ == '__main__':
    unittest.main()
