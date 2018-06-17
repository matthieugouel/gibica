"""Lexer module."""

from gibica.lexer.token import Token
from gibica.lexer.token import Name

#
# Lexical Analysis
#

# List of reserved keywords
RESERVED_KEYWORDS: dict = {
    'int': Token(Name.INT, 'int'),
    'float': Token(Name.FLOAT, 'float'),
    'mut': Token(Name.MUT, 'mut')
}


class Lexer(object):
    """Lexical analyser."""

    def __init__(self, raw):
        self.raw = raw
        self.cursor = 0
        self.char = self.raw[self.cursor]

    def advance(self):
        """Increments the cursor position."""
        self.cursor += 1
        if self.cursor >= len(self.raw):
            self.char = None
        else:
            self.char = self.raw[self.cursor]

    def peek(self):
        peek_cursor = self.cursor + 1
        if peek_cursor >= len(self.raw):
            return None
        else:
            return self.raw[peek_cursor]

    def whitespace(self):
        """Handle whitespace."""
        while self.char is not None and self.char.isspace():
            self.advance()

    def comment(self):
        while self.char != '*' or self.peek() != '/':
            self.advance()
        self.advance()
        self.advance()

    def number(self):
        """Return a multidigit int or float number."""
        number = ''
        while self.char is not None and self.char.isdigit():
            number += self.char
            self.advance()

        if self.char == '.':
            number += self.char
            self.advance()

            while self.char is not None and self.char.isdigit():
                number += self.char
                self.advance()

            token = Token(Name.FLOAT_NUMBER, float(number))

        else:
            token = Token(Name.INT_NUMBER, int(number))

        return token

    def _id(self):
        """Handle identifiers and reserverd keywords."""
        result = ''
        while self.char is not None and self.char.isalnum():
            result += self.char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(Name.ID, result))
        return token

    def next_token(self):
        """Lexical analyser of the raw input."""
        while self.char is not None:
            if self.char.isspace():
                # The current character is a whitespace
                self.whitespace()
                continue
            elif self.char.isalpha():
                # The curent character is a letter
                return self._id()
            elif self.char == '=':
                self.advance()
                return Token(Name.ASSIGN, '=')
            elif self.char == ';':
                self.advance()
                return Token(Name.SEMI, ';')
            elif self.char.isdigit():
                # The current character is a number
                return self.number()
            elif self.char == '+':
                # The current character is `+`
                self.advance()
                return Token(Name.PLUS, '+')
            elif self.char == '-':
                # The current character is `-`
                self.advance()
                return Token(Name.MINUS, '-')
            elif self.char == '*':
                # The current character is `*`
                self.advance()
                return Token(Name.MUL, '*')
            elif self.char == '/':
                if self.peek() == '/':
                    # The current character is `//`
                    self.advance()
                    self.advance()
                    return Token(Name.INT_DIV, '//')
                elif self.peek() == '*':
                    # The current character is `/*
                    self.advance()
                    self.advance()
                    self.comment()
                    continue
                else:
                    # The current character is `/`
                    self.advance()
                    return Token(Name.DIV, '/')
            elif self.char == '(':
                # The current character is `(`
                self.advance()
                return Token(Name.LPAREN, '(')
            elif self.char == ')':
                # The current character is `)`
                self.advance()
                return Token(Name.RPAREN, ')')
            else:
                # The current character is unknown
                raise Exception(f'LEXICAL: Invalid character `{self.char}`.')

        # End of raw input
        return Token(Name.EOF, None)