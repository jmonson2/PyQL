from typing import List, Optional
from src.parser.tokens import Token, TokenType
from src.parser.ast import (
    ASTNode, CreateTableStatement, ColumnDef, InsertStatement, SelectStatement
)
from src.parser.errors import ParserError

class Parser:
    """
    A recursive descent parser that transforms a stream of Tokens into an Abstract Syntax Tree (AST).
    """
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1] # EOF

    def consume(self, expected_type: TokenType) -> Token:
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise ParserError(f"Expected {expected_type.name}, got {token.type.name} at line {token.line}:{token.column}")

    def parse(self) -> List[ASTNode]:
        """Parse all statements in the token stream."""
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
                
            # Optional semicolon
            if self.current_token().type == TokenType.SEMICOLON:
                self.consume(TokenType.SEMICOLON)
            elif self.current_token().type == TokenType.EOF:
                break
            else:
                raise ParserError(f"Unexpected token {self.current_token().type.name} between statements.")
                
        return statements

    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single SQL statement."""
        token = self.current_token()
        if token.type == TokenType.CREATE:
            return self.parse_create_table()
        elif token.type == TokenType.INSERT:
            return self.parse_insert()
        elif token.type == TokenType.SELECT:
            return self.parse_select()
        else:
            raise ParserError(f"Unexpected token {token.type.name} at line {token.line}:{token.column}")

    def parse_create_table(self) -> CreateTableStatement:
        self.consume(TokenType.CREATE)
        self.consume(TokenType.TABLE)
        table_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LPAREN)
        
        columns = []
        while self.current_token().type != TokenType.RPAREN:
            col_name = self.consume(TokenType.IDENTIFIER).value
            col_type = self.consume(TokenType.IDENTIFIER).value.upper()
            
            length = 0
            # E.g., VARCHAR(10)
            if self.current_token().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                length = int(self.consume(TokenType.NUMBER_LITERAL).value)
                self.consume(TokenType.RPAREN)
                
            columns.append(ColumnDef(col_name, col_type, length))
            
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
                
        self.consume(TokenType.RPAREN)
        return CreateTableStatement(table_name, columns)

    def parse_insert(self) -> InsertStatement:
        self.consume(TokenType.INSERT)
        self.consume(TokenType.INTO)
        table_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.VALUES)
        self.consume(TokenType.LPAREN)
        
        values = []
        while self.current_token().type != TokenType.RPAREN:
            token = self.current_token()
            if token.type == TokenType.NUMBER_LITERAL:
                val_str = self.consume(TokenType.NUMBER_LITERAL).value
                if '.' in val_str:
                    values.append(float(val_str))
                else:
                    values.append(int(val_str))
            elif token.type == TokenType.STRING_LITERAL:
                # Remove surrounding quotes
                val_str = self.consume(TokenType.STRING_LITERAL).value[1:-1]
                values.append(val_str)
            elif token.type == TokenType.IDENTIFIER:
                # Handle booleans TRUE/FALSE
                val_str = self.consume(TokenType.IDENTIFIER).value.upper()
                if val_str == "TRUE":
                    values.append(True)
                elif val_str == "FALSE":
                    values.append(False)
                else:
                    raise ParserError(f"Unexpected identifier {val_str} in VALUES clause")
            else:
                raise ParserError(f"Unexpected token {token.type.name} in VALUES clause")
                
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
                
        self.consume(TokenType.RPAREN)
        return InsertStatement(table_name, values)

    def parse_select(self) -> SelectStatement:
        self.consume(TokenType.SELECT)
        
        columns = []
        if self.current_token().type == TokenType.ASTERISK:
            self.consume(TokenType.ASTERISK)
        else:
            while True:
                col_name = self.consume(TokenType.IDENTIFIER).value
                columns.append(col_name)
                if self.current_token().type == TokenType.COMMA:
                    self.consume(TokenType.COMMA)
                else:
                    break
                    
        self.consume(TokenType.FROM)
        table_name = self.consume(TokenType.IDENTIFIER).value
        
        return SelectStatement(table_name, columns)
