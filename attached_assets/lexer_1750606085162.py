"""
VibeScript Lexer

This module tokenizes VibeScript source code.
"""

import re
from vibescript.grammar import TOKEN_TYPES, KEYWORDS

class Token:
    """Represents a token in the VibeScript language"""
    
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f'Token({self.type}, {repr(self.value)}, position={self.line}:{self.column})'
    
    def __repr__(self):
        return self.__str__()

class LexerError(Exception):
    """Exception raised when an error occurs during lexical analysis"""
    
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"{message} at line {line}, column {column}")

class Lexer:
    """Lexical analyzer for VibeScript"""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None
        self.line = 1
        self.column = 1
    
    def error(self, message):
        """Raise a lexer error with the current position"""
        raise LexerError(message, self.line, self.column)
    
    def advance(self):
        """Advance the position pointer and set the current character"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1
    
    def peek(self, n=1):
        """Look ahead n characters without advancing"""
        peek_pos = self.pos + n
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments starting with '//'"""
        # Skip the '//' markers
        self.advance()
        self.advance()
        
        # Skip everything until the end of the line
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
            
        # Skip the newline
        if self.current_char == '\n':
            self.advance()
    
    def number(self):
        """Process a numeric literal"""
        start_column = self.column
        result = ''
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
        return Token(TOKEN_TYPES['INTEGER'], int(result), self.line, start_column)
    
    def string(self):
        """Process a string literal"""
        start_column = self.column
        # Skip the opening quote
        self.advance()
        
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()  # Skip the backslash
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    self.error(f"Invalid escape sequence: \\{self.current_char}")
            else:
                result += self.current_char
            
            self.advance()
        
        if self.current_char != '"':
            self.error("Unterminated string literal")
            
        # Skip the closing quote
        self.advance()
        
        return Token(TOKEN_TYPES['STRING'], result, self.line, start_column)
    
    def identifier(self):
        """Process an identifier or keyword"""
        start_column = self.column
        result = ''
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        # Check if the identifier is a keyword
        token_type = KEYWORDS.get(result, TOKEN_TYPES['IDENTIFIER'])
        
        return Token(token_type, result, self.line, start_column)
    
    def get_next_token(self):
        """Get the next token from the input"""
        while self.current_char is not None:
            
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Identifier or keyword
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Number
            if self.current_char.isdigit():
                return self.number()
            
            # String
            if self.current_char == '"':
                return self.string()
            
            # Operators and delimiters
            if self.current_char == '+':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['PLUS'], '+', self.line, col)
                
            if self.current_char == '-':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['MINUS'], '-', self.line, col)
                
            if self.current_char == '*':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['MULTIPLY'], '*', self.line, col)
                
            if self.current_char == '/':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['DIVIDE'], '/', self.line, col)
                
            if self.current_char == '=':
                col = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TOKEN_TYPES['EQUALS'], '==', self.line, col)
                return Token(TOKEN_TYPES['ASSIGN'], '=', self.line, col)
                
            if self.current_char == '!':
                col = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TOKEN_TYPES['NOT_EQUALS'], '!=', self.line, col)
                self.error("Expected '=' after '!'")
                
            if self.current_char == '<':
                col = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TOKEN_TYPES['LESS_EQUALS'], '<=', self.line, col)
                return Token(TOKEN_TYPES['LESS_THAN'], '<', self.line, col)
                
            if self.current_char == '>':
                col = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TOKEN_TYPES['GREATER_EQUALS'], '>=', self.line, col)
                return Token(TOKEN_TYPES['GREATER_THAN'], '>', self.line, col)
                
            if self.current_char == '(':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['LPAREN'], '(', self.line, col)
                
            if self.current_char == ')':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['RPAREN'], ')', self.line, col)
                
            if self.current_char == '[':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['LBRACKET'], '[', self.line, col)
                
            if self.current_char == ']':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['RBRACKET'], ']', self.line, col)
                
            if self.current_char == ',':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['COMMA'], ',', self.line, col)
                
            if self.current_char == ';':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['SEMICOLON'], ';', self.line, col)
                
            if self.current_char == ':':
                col = self.column
                self.advance()
                return Token(TOKEN_TYPES['COLON'], ':', self.line, col)
            
            # If we get here, we have an unrecognized character
            self.error(f"Unrecognized character: '{self.current_char}'")
        
        # End of file
        return Token(TOKEN_TYPES['EOF'], None, self.line, self.column)
    
    def tokenize(self):
        """Tokenize the entire input and return a list of tokens"""
        tokens = []
        token = self.get_next_token()
        
        while token.type != TOKEN_TYPES['EOF']:
            tokens.append(token)
            token = self.get_next_token()
            
        tokens.append(token)  # Add EOF token
        return tokens
