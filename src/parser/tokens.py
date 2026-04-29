from enum import Enum, auto
from typing import NamedTuple, Pattern

class TokenType(Enum):
    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AND = auto()
    OR = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    UPDATE = auto()
    SET = auto()
    DELETE = auto()
    CREATE = auto()
    TABLE = auto()
    
    # Literals and Identifiers
    IDENTIFIER = auto()
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()
    
    # Operators and Symbols
    EQUALS = auto()
    COMMA = auto()
    ASTERISK = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    
    # Special
    EOF = auto()
    ILLEGAL = auto()

# Dictionary for fast keyword lookup
KEYWORDS = {
    'SELECT': TokenType.SELECT,
    'FROM': TokenType.FROM,
    'WHERE': TokenType.WHERE,
    'AND': TokenType.AND,
    'OR': TokenType.OR,
    'INSERT': TokenType.INSERT,
    'INTO': TokenType.INTO,
    'VALUES': TokenType.VALUES,
    'UPDATE': TokenType.UPDATE,
    'SET': TokenType.SET,
    'DELETE': TokenType.DELETE,
    'CREATE': TokenType.CREATE,
    'TABLE': TokenType.TABLE,
}

class Token(NamedTuple):
    type: TokenType
    value: str
    line: int
    column: int

class TokenDefinition(NamedTuple):
    type: TokenType
    pattern: Pattern
