import re
from typing import List
from .tokens import TokenType, Token, TokenDefinition, KEYWORDS
from .errors import LexerError

class Lexer:
    """
    A simple, extensible lexical analyzer for SQL statements.
    It uses a regex definition list combined with a keyword dictionary lookup.
    """
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Define token patterns. 
        # Keywords are no longer defined here; they are matched as IDENTIFIERs first, 
        # then looked up in the KEYWORDS dictionary.
        self.token_definitions: List[TokenDefinition] = [
            # Symbols and Operators
            TokenDefinition(TokenType.EQUALS, re.compile(r'=')),
            TokenDefinition(TokenType.COMMA, re.compile(r',')),
            TokenDefinition(TokenType.ASTERISK, re.compile(r'\*')),
            TokenDefinition(TokenType.LPAREN, re.compile(r'\(')),
            TokenDefinition(TokenType.RPAREN, re.compile(r'\)')),
            TokenDefinition(TokenType.SEMICOLON, re.compile(r';')),
            
            # Literals and Identifiers
            TokenDefinition(TokenType.STRING_LITERAL, re.compile(r"'[^']*'")),
            TokenDefinition(TokenType.NUMBER_LITERAL, re.compile(r'\b\d+(\.\d+)?\b')),
            TokenDefinition(TokenType.IDENTIFIER, re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')),
        ]
        
        # Regex for whitespace and newlines
        self.whitespace_pattern = re.compile(r'[ \t\r]+')
        self.newline_pattern = re.compile(r'\n')

    def _advance_position(self, length: int):
        """Helper to advance the position and handle column tracking."""
        self.pos += length
        self.column += length

    def _skip_whitespace(self):
        """Skips whitespaces and newlines, updating line and column accordingly."""
        while self.pos < len(self.text):
            # Check for newlines first to update line counts
            newline_match = self.newline_pattern.match(self.text, self.pos)
            if newline_match:
                self.pos += 1
                self.line += 1
                self.column = 1
                continue
            
            # Check for other whitespaces
            ws_match = self.whitespace_pattern.match(self.text, self.pos)
            if ws_match:
                self._advance_position(len(ws_match.group(0)))
                continue
                
            break # No more whitespace

    def next_token(self) -> Token:
        """
        Retrieves the next token from the input stream.
        """
        self._skip_whitespace()
        
        if self.pos >= len(self.text):
            return Token(TokenType.EOF, "", self.line, self.column)
            
        remaining_text = self.text[self.pos:]
        
        for token_def in self.token_definitions:
            match = token_def.pattern.match(self.text, self.pos)
            if match:
                value = match.group(0)
                token_type = token_def.type
                
                # Keyword lookup: if it's an identifier, check if it's actually a keyword
                if token_type == TokenType.IDENTIFIER:
                    token_type = KEYWORDS.get(value.upper(), TokenType.IDENTIFIER)
                
                token = Token(token_type, value, self.line, self.column)
                self._advance_position(len(value))
                return token
                
        # If no pattern matches, raise an error
        raise LexerError(f"Illegal character: '{self.text[self.pos]}'", self.line, self.column)

    def tokenize(self) -> List[Token]:
        """
        Helper method to generate all tokens for the input string.
        """
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
