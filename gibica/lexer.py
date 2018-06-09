"""Lexer."""


#
# Lexical Analysis
#

# List of reserved keywords
RESERVED_KEYWORDS: dict = {}


class Type(object):
    """Enumeration of token types."""

    ID = 'ID'
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    ASSIGN = 'ASSIGN'
    SEMI = 'SEMI'
    EOF = 'EOF'


class Token(object):
    """Construct a token."""

    def __init__(self, type, value):
        """Initialization of `Token` class."""
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of a token."""
        return f"Token({self.type}, {self.value})"

    def ___repr__(self):
        """String representation of the class."""
        return self.__str__()


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

    def whitespace(self):
        """Handle whitespace."""
        while self.char is not None and self.char.isspace():
            self.advance()

    def integer(self):
        """Return a multidigit integer."""
        number = ''
        while self.char is not None and self.char.isdigit():
            number += self.char
            self.advance()
        return int(number)

    def _id(self):
        """Handle identifiers and reserverd keywords."""
        result = ''
        while self.char is not None and self.char.isalnum():
            result += self.char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(Type.ID, result))
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
                return Token(Type.ASSIGN, '=')
            elif self.char == ';':
                self.advance()
                return Token(Type.SEMI, ';')
            elif self.char.isdigit():
                # The current character is an integer
                return Token(Type.INTEGER, self.integer())
            elif self.char == '+':
                # The current character is `+`
                self.advance()
                return Token(Type.PLUS, '+')
            elif self.char == '-':
                # The current character is `-`
                self.advance()
                return Token(Type.MINUS, '-')
            elif self.char == '*':
                # The current character is `*`
                self.advance()
                return Token(Type.MUL, '*')
            elif self.char == '/':
                # The current character is `/`
                self.advance()
                return Token(Type.DIV, '/')
            elif self.char == '(':
                # The current character is `(`
                self.advance()
                return Token(Type.LPAREN, '(')
            elif self.char == ')':
                # The current character is `)`
                self.advance()
                return Token(Type.RPAREN, ')')
            else:
                # The current character is unknown
                raise Exception(f'LEXICAL: Invalid character `{self.char}`.')

        # End of raw input
        return Token(Type.EOF, None)
