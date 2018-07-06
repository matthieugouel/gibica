"""Lexer module."""

from gibica.tokens import Token, Name, RESERVED_KEYWORDS
from gibica.exceptions import LexicalError


#
# Lexical Analysis
#


class Lexer(object):
    """Lexical analyser."""

    def __init__(self, raw):
        """Initialization of `Lexer` class."""
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
        """Get the next character without moving the cursor."""
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
        """Handle comments."""
        while self.char is not None and self.char != '\n':
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

            token = Token(Name.FLOAT_NUMBER, number)

        else:
            token = Token(Name.INT_NUMBER, number)

        return token

    def _id(self):
        """Handle identifiers and reserverd keywords."""
        result = ''
        while self.char is not None and (self.char.isalnum() or self.char == '_'):
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

            elif self.char == '#':
                # The current character is `#`
                self.advance()
                self.comment()
                continue

            elif self.char.isalpha() or self.char == '_':
                # The curent character is a letter or `_`
                return self._id()

            elif self.char == ';':
                # The current character is `;`
                self.advance()
                return Token(Name.SEMI, ';')

            elif self.char == ',':
                # The current character is `,`
                self.advance()
                return Token(Name.COMMA, ';')

            elif self.char.isdigit():
                # The current character is a number
                return self.number()

            elif self.char == '=' and self.peek() == '=':
                # The current character is `==`
                self.advance()
                self.advance()
                return Token(Name.EQ, '==')

            elif self.char == '!' and self.peek() == '=':
                # The current character is `!=`
                self.advance()
                self.advance()
                return Token(Name.NE, '!=')

            elif self.char == '<' and self.peek() == '=':
                # The current character is `<=`
                self.advance()
                self.advance()
                return Token(Name.LE, '<=')

            elif self.char == '>' and self.peek() == '=':
                # The current character is `>=`
                self.advance()
                self.advance()
                return Token(Name.GE, '>=')

            elif self.char == '<':
                # The current character is `<`
                self.advance()
                return Token(Name.LT, '<')

            elif self.char == '>':
                # The current character is `>`
                self.advance()
                return Token(Name.GT, '>')

            elif self.char == '=':
                # The current character is `=`
                self.advance()
                return Token(Name.ASSIGN, '=')

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

            elif self.char == '/' and self.peek() == '/':
                # The current character is `//`
                self.advance()
                self.advance()
                return Token(Name.INT_DIV, '//')

            elif self.char == '/':
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

            elif self.char == '{':
                # The current character is `{`
                self.advance()
                return Token(Name.LBRACKET, '{')

            elif self.char == '}':
                # The current character is `}`
                self.advance()
                return Token(Name.RBRACKET, '}')

            else:
                # The current character is unknown
                raise LexicalError(f"Invalid character `{self.char}`.")

        # End of raw input
        return Token(Name.EOF, None)
